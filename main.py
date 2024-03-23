from flask import Flask
from flask_restful import Api
# Resources provide a structured way of organizing API endpoints, by
# defining classes that inhereit from (are subclasses of) the Resource class.
# Each instance method in the Resource parent class is catered to a
# specific HTTP request method (get(), put(), post(), delete()).
from flask_restful import Resource
# Makes sure that we pass the information that we need with each request.
from flask_restful import reqparse
# Alows us to send an error message upon abort.
from flask_restful import abort


# Note: Whenever we send a request, it will be to localhost:5000/

app = Flask(__name__)
# Initializes a RESTful API.
api = Api(app)

# Makes a new request parser object.  It will parse the request being sent 
# and make sure it has the information that we need in it.
video_put_args = reqparse.RequestParser()
# One of the pieces of information that needs to be included in the request.
# The first argument is the key, the type of the key, and a error message to
# display if this piece of information if not included with the request.
# required means it's required.
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video is required", required=True)

videos = {}

# Function to abort if user tries to get information for a video that is not
# in the dictionary.
def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        # Method requires a status code and a message to send.
        abort(404, message="Video id is not valid.")

class Video(Resource):
    def get(self, video_id):
        # See if we need to abort.
        abort_if_video_id_doesnt_exist(video_id)
        # Return any information about the video.
        return videos[video_id]
    
    def put(self, video_id):
        # Parse the request to make sure the request contains all the necessary
        # information for adding a video.
        args = video_put_args.parse_args()
        # At this point, request has been verified to contain all necessary
        # information.  Add a new entry to our videos dictionary, using the
        # video_id as the key and the information passed in the request as the
        # value.
        videos[video_id] = args
        # Return success.
        return videos[video_id], 201
    
api.add_resource(Video, "/video/<int:video_id>")



## Examples ##

# Making a resource.  
class HelloWorld(Resource):
    # Overriding the get() method, which means this is what will happen 
    # when we send a GET request to a certain URL.
    def get(self, name):
        return {"data" : "Hello World"}
    
class HelloWorld2(Resource):
    def get(self, name, test):
        return {"name" : name, "test number": test}
        
# Register the resource with the API.  "/helloworld" is the endpoint we 
# will make the resource accessible from.  Now, if we send a GET request
# to /helloworld, we will see the information, "Hello World".
api.add_resource(HelloWorld, "/helloworld/<string:name>")

# We can have the user type in a string value after /helloworld/ , pass
# that value to our get() method, and use it in some way in our definition.
# This can be done using multiple variables, like including an int after.
api.add_resource(HelloWorld2, "/helloworld/<string:name>/<int:test>")

## End examples ##

if __name__ == "__main__":
    # Only run debug=True in development. In production, run debug=False.
    app.run(debug=True) 
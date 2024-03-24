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

from flask_sqlalchemy import SQLAlchemy

from flask_restful import fields, marshal_with


# Note: Whenever we send a request, it will be to localhost:5000/

# Initializes the Flask application.
app = Flask(__name__)
# Initializes a RESTful API.
api = Api(app)
# Defining the location we'd like our database to be, which will be in our 
# main project directory in a file named database.db.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Initializes our database.
db = SQLAlchemy(app)

# Create a model, which will be a subclass of our database, 'db'.
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Setting max characters allowed to 100.  nullable=false means we have 
    # to include a value for this field.
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    

# Creates all the database tables defined in our models.  Make sure you 
# put this line after all your model definitions.  Then, run this file once
# to create the database, and then delete this line so it is not run again
# next time you run the file.  Doing so would recreate the table and wipe all
# previous data from it.
## db.create_all()

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

# Resource fields are a way to define how an object should be serialized.
# This dictionary defines the fields from the VideoModel that we want to return
# when we return a VideoModel.
resource_fields = {
    'id' : fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

# Function to abort if user tries to get information for a video that is not
# in the dictionary.
def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        # Method requires a status code and a message to send.
        abort(404, message="Video id is not valid.")

# Function to abort if user tries to put a video that has already been put
# before.
def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="Video already exists with that ID.")

class Video(Resource):
    # Tells this function to take what it is set to return and serialize it
    # with resource_fields.
    @marshal_with(resource_fields)
    def get(self, video_id):
        # # See if we need to abort.
        # abort_if_video_id_doesnt_exist(video_id)
        # # Return any information about the video.
        # return videos[video_id]
        
        # Query the database for the video that matches the video id
        # we're looking for.   
        # filter_by() filters the query results to only those videos that
        # have an id that matches our video_id. Then, first() selects the
        # first one.
        result = VideoModel.query.filter_by(id=video_id).first()
        # Result is an instance of VideoModel, which will be transformed
        # into a dictionary by the marshal_with decorator.
        return result
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        # # If the video has already been previously put, abort.
        # abort_if_video_exists(video_id)
        # # Parse the request to make sure the request contains all the necessary
        # # information for adding a video.
        # args = video_put_args.parse_args()
        # # At this point, request has been verified to contain all necessary
        # # information.  Add a new entry to our videos dictionary, using the
        # # video_id as the key and the information passed in the request as the
        # # value.
        # videos[video_id] = args
        # # Return success.
        # return videos[video_id], 201
        
        
        # Parse the request to make sure the request contains all the necessary
        #  information for adding a video.
        args = video_put_args.parse_args()
        # Query the database for the video that matches the video id
        # we're looking for. 
        result = VideoModel.query.filter_by(id=video_id).first()
        # Check to see if the query by video_id produced a result.
        if result:
            # In which case, we can't add it to the database because it's 
            # already there.
            abort(409, message="Video id taken.")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        # Add video to the database staging area.
        db.session.add(video)
        # Commit all the additions in the staging area.
        db.session.commit()
        
        return video, 201
        
        
    def delete(self, video_id):
        # If video to delete does not exist, abort.
        abort_if_video_id_doesnt_exist(video_id)
        # Otherwise, delete video.
        del videos[video_id]
        # Return deleted successfully status code with no message.
        return '', 204
        
# Add the Video resource to the API, and make it accessible at .../video/
# followed by the video_id.    
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
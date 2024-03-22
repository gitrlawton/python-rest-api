from flask import Flask
from flask_restful import Api
# Resources provide a structured way of organizing API endpoints, by
# defining classes that inhereit from (are subclasses of) the Resource class.
# Each instance method in the Resource parent class is catered to a
# specific HTTP request method (get(), put(), post(), delete()).
from flask_restful import Resource

# Note: Whenever we send a request, it will be to localhost:5000/

app = Flask(__name__)
# Initializes a RESTful API.
api = Api(app)


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

if __name__ == "__main__":
    # Only run debug=True in development. In production, run debug=False.
    app.run(debug=True) 
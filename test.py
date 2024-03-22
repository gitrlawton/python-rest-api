import requests

# Our local host server.
BASE = "http://127.0.0.1:5000/"

# BASE + "helloworld" concatenates the two into the endpoint we are
# trying to reach (localhost:5000/helloworld)
response = requests.get(BASE + "helloworld")
# Parse the response object to json and print it.
print(response.json())
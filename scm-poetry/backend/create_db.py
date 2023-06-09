import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()  # read local .env file
uri = os.environ.get("POETRY_MONGODB_URL")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Create a database named "mydatabase"
mydb = client["messagesdb"]

# Create a collection named "customers"
mycol = mydb["slackcollection"]

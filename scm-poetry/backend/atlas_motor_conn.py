import os

import motor
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()  # read local .env file
uri = os.environ.get("POETRY_MONGODB_URL")

# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["POETRY_MONGODB_URL"])

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

import os

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()  # read local .env file


async def ping_server():
    # Replace the placeholder with your Atlas connection string
    uri = os.environ.get("POETRY_MONGODB_URL")
    # Set the Stable API version when creating a new client
    client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. Successfly connected to MongoDB using asyncio!")
    except Exception as e:
        print(e)


asyncio.run(ping_server())

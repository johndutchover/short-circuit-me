import datetime
import os
import pathlib
import re


from dotenv import load_dotenv
from fastapi import FastAPI, Request
from motor import motor_asyncio
from pydantic import BaseModel
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

cfd = pathlib.Path(__file__).parent
message_counts_path = cfd / "message_counts.csv"

load_dotenv()  # read local .env file


# Define the data model
class Item(BaseModel):
    date: str
    count1: int
    flag: int
    count2: int


# MongoDB Atlas connection string
uri = os.environ.get("POETRY_MONGODB_URL")

# Set the Stable API version when creating a new client
client = motor_asyncio.AsyncIOMotorClient(os.environ["POETRY_MONGODB_URL"])
# database name in MongoDB
db = client["messagesdb"]
# collection name in MongoDB
collection = db["slackcoll"]

# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    # signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET") # not required for socket mode
)
app_handler = SlackRequestHandler(app)
api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    """
    endpoint which handles incoming requests from Slack
    :param req:
    :return:
    """
    return await app_handler.handle(req)


string_pattern_help = r"(?:help)"
regex_help = re.compile(string_pattern_help, flags=re.I)
string_pattern_important = r"(?:important)"
regex_important = re.compile(string_pattern_important, flags=re.I)
string_pattern_hello = r"(?:hello)"
regex_p3 = re.compile(string_pattern_hello, flags=re.I)


async def increase_counter(message_type: str):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    current_data = await collection.find_one({"date": formatted_date})

    if current_data is None:
        new_data = {
            "date": formatted_date,
            "normal": 0,
            "important": 0,
            "urgent": 0
        }
        await collection.insert_one(new_data)
    else:
        new_data = current_data

    if message_type in new_data:
        new_data[message_type] += 1
        await collection.replace_one({"date": formatted_date}, new_data)
    else:
        print(f"{message_type} is not a valid key in the document")


# Start app using WebSockets
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["POETRY_SCM_XAPP_TOKEN"]).start()

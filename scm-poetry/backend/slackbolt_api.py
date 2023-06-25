import datetime
import os
import re

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from motor import motor_asyncio
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

load_dotenv()  # read local .env file

bolt = AsyncApp(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET")
)

api = FastAPI()

app_handler = AsyncSlackRequestHandler(bolt)

# Initialize a contact dictionary
contacts = {}

bots_clientid = os.getenv('POETRY_SCM_BOT_CLIENTID')

# Users who are allowed to use the commands
allowed_users = ["USLACKBOT", bots_clientid]

# MongoDB connection string
uri = os.environ.get("POETRY_MONGODB_URL")
# Set the Stable API version when creating a new client
client = motor_asyncio.AsyncIOMotorClient(uri)
# database name in MongoDB
db = client["messagesdb"]
# collection name in MongoDB
collection = db["slackcoll"]


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


async def increase_counter(message_type: str):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    current_data = collection.find_one({"msg_date": formatted_date})

    if current_data is None:
        new_data = {
            "msg_date": formatted_date,
            "normal": 0,
            "important": 0,
            "urgent": 0
        }
        await collection.insert_one(new_data)
    else:
        new_data = current_data

    if message_type in new_data:
        new_data[message_type] += 1
        await collection.replace_one({"msg_date": formatted_date}, new_data)
    else:
        print(f"{message_type} is not a valid key in the document")


@bolt.message(re.compile("(asap|help|urgent)", re.I))
async def message_urgent(message, say):
    await say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Do you need help <@{message['user']}>?"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click to escalate"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )
    await increase_counter('urgent')


@bolt.message(re.compile("(important|priority|soon)", re.I))
async def message_important(message, say):
    await say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"<@{message['user']}> Can it wait until Monday?"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click to record a message"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Please record at this time <@{message['user']}>!"
    )
    await increase_counter('important')


@bolt.message(re.compile("(hi|hello|hey)", re.I))
async def say_hello_regex(say, context):
    greeting = context['matches'][0]
    await say(f"{greeting}, how are you?")
    user_id = "test"
    await increase_counter_based_on_user_id(user_id=user_id)


async def increase_counter_based_on_user_id(user_id: str):
    if user_id in contacts.keys():
        await increase_counter("important")
    else:
        await increase_counter("normal")


async def main():
    handler = AsyncSocketModeHandler(bolt, os.environ["POETRY_SCM_XAPP_TOKEN"])
    await handler.start_async()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

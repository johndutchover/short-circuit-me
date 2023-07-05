import datetime
import os
import re

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from motor import motor_asyncio
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from slack_bolt.context.async_context import AsyncBoltContext
from slack_sdk.web.async_client import AsyncWebClient

load_dotenv()  # read local .env file

bolt = AsyncApp(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET")
)

api = FastAPI()

app_handler = AsyncSlackRequestHandler(bolt)

# Initialize a contact dictionary
my_contacts = {}

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


# Slash command help-slack-bolt
@bolt.command("/help-slack-bolt")
async def slash_help(ack, body):
    user_id = body["user_id"]
    await ack(f"Request for help has been sent <@{user_id}>!")


# Slash command add-contact
@bolt.command("/add-contact")
async def add_contact(ack, respond, commandadd):
    # Acknowledge command request
    ack()

    # Get user's ID from the command text
    user_id = await commandadd['text']

    provided_id_has_correct_format = re.match("^U[A-Z0-9]{8,}$", user_id)
    if provided_id_has_correct_format:
        # Add user to contacts
        my_contacts[user_id] = user_id
        # Respond with success message
        respond(f"User {user_id} added to contacts.")
    else:
        respond("Invalid format. Please provide a valid Slack User ID.")


# Slash command that retrieves a contact
@bolt.command("/get-contact")
async def get_contact(ack, respond, commandget):
    # Acknowledge command request
    ack()

    user_id = await commandget['text']
    if user_id in my_contacts:
        respond(f"Contact found for User ID: {my_contacts[user_id]}")
    else:
        respond(f"No contact found for User ID: {user_id}")


async def increase_counter(message_type: str):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    current_data = await collection.find_one({"msg_date": formatted_date})

    if current_data is None:
        new_data = {
            "msg_date": formatted_date,
            "normal": 0,
            "priority": 0,
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


@bolt.message(re.compile("(asap|help|critical)", re.I))
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


@bolt.message(re.compile("(important|urgent|soon)", re.I))
async def message_priority(message, say):
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
    await increase_counter('priority')


@bolt.message(re.compile("(hi|hello|hey)", re.I))
async def say_hello_regex(say, context):
    greeting = context['matches'][0]
    await say(f"{greeting}, how are you?")
    user_id = "U059Y617831"
    await increase_counter_based_on_user_id(user_id=user_id)


@bolt.event("message")
async def check_starred(context: AsyncBoltContext, message: dict, starredcontacts: AsyncWebClient):
    bot_id = context.bot_user_id
    # Get the list of items starred by the bot
    result = await starredcontacts.stars_list(user=bot_id)
    # Check if the received message is in the list of starred items
    for item in result['items']:
        if 'message' in item and item['message']['ts'] == message['ts']:
            print("starred")
            await increase_counter_based_on_user_id(user_id=bot_id)


async def increase_counter_based_on_user_id(user_id: str):
    if user_id in my_contacts.keys():
        await increase_counter("priority")
    else:
        await increase_counter("normal")


async def main():
    handler = AsyncSocketModeHandler(bolt, os.environ["POETRY_SCM_XAPP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

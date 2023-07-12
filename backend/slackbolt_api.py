import asyncio
import datetime
import logging
import os
import re

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from motor import motor_asyncio
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.async_app import AsyncApp
from slack_sdk.errors import SlackApiError

load_dotenv()  # read local .env file

logger_slackbolt = logging.getLogger(__name__)

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
allowed_bot_users = ["USLACKBOT", bots_clientid]

# MongoDB connection string
uri = os.environ["POETRY_MONGODB_URL"]
# Set the Stable API version when creating a new client
client = motor_asyncio.AsyncIOMotorClient(uri)
# database name in MongoDB
db = client["messagesdb"]
# collection name in MongoDB
collection = db["slackcoll"]


# API Endpoint - FastAPI
@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


# Listen for event from Events API
@bolt.event("app_mention")
async def mention_handler(body, say):
    user = body['event']['user']
    await say(f'Hello, <@{user}>!')


# Listen for event from Events API
@bolt.event("messages.mpim")
async def mention_handler(body, say):
    user = body['event']['user']
    await say(f'Multi-party Hello, <@{user}>!')


# Listen for event from Events API
@bolt.event("messages.im")
async def mention_handler(body, say):
    user = body['event']['user']
    await say(f'DM Hello, <@{user}>!')


# Slack ACTION Handler
@bolt.action("action_button_notify")
async def handle_button_escalate(ack, body):  # method is a callback for Slack button action
    # Acknowledge the action request
    await ack()

    # Extract information from the action payload
    channel_id = body["channel"]["id"]  # Get the ID of the channel

    # perform action
    await bolt.client.chat_postMessage(
        channel=channel_id,
        text="Notify Button clicked!",
        blocks=[
            {
                "type": "divider",
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Choose one:*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Escalate - it is urgent:"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Escalate immediately",
                    },
                    "value": "click_button_urgent",
                    "action_id": "click_button_urgent"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Important - but it can wait:"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Notify tomorrow at 09:00",
                    },
                    "value": "click_button_important",
                    "action_id": "click_button_important"
                }
            }
        ],
    )


@bolt.action("click_button_urgent")
async def handle_urgent_button_click(ack, body):
    # Acknowledge the button request
    await ack()

    # Perform your action here for the "Escalate immediately" button
    await bolt.client.chat_postMessage(
        channel=body['user']['id'],
        text="Urgent escalation in process!",
        response_type="ephemeral"
    )


@bolt.action("click_button_important")
async def handle_important_button_click(ack, body):
    # Acknowledge the button request
    await ack()

    # Create a timestamp for tomorrow at 8:40 AM
    tomorrow = datetime.date.today() + datetime.timedelta(days=0)
    scheduled_time = datetime.time(hour=8, minute=56)
    schedule_timestamp = datetime.datetime.combine(tomorrow, scheduled_time).strftime('%s')

    try:
        # Call the chat.scheduleMessage method using the WebClient
        result = await bolt.client.chat_scheduleMessage(
            channel=body['user']['id'],
            text=f"Your issue will be addressed on {schedule_timestamp}.",
            response_type="ephemeral",
            post_at=schedule_timestamp,
            token=bolt.client.token
        )
        # Log the result
        logger_slackbolt.info(result)

    except SlackApiError as e:
        logger_slackbolt.error("Error scheduling message: {}".format(e))


# Slack MESSAGE Handler: convenience method to listen for `message` events (urgent)
@bolt.message(re.compile("(asap|critical|urgent)", re.I))
async def message_urgent(message, say):
    await say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Do you need urgent help <@{message['user']}>?"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click to escalate"},
                    "action_id": "action_button_notify"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )
    await increase_counter('urgent')


# Slack MESSAGE Handler: convenience method to listen for `message` events (priority)
@bolt.message(re.compile("(important|help|soon)", re.I))
async def message_priority(message, say):
    await say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"<@{message['user']}> Important message menu:"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click here."},
                    "action_id": "action_button_notify"
                }
            }
        ],
        text=f"<@{message['user']}> recorded!"
    )
    await increase_counter('priority')


# Slack MESSAGE Handler: convenience method to listen for `message` events (normal)
@bolt.message(re.compile("(hi|hello|hey)", re.I))
async def message_normal(say, context):
    greeting = context['matches'][0]
    await say(f"{greeting}, how are you?")
    await increase_counter("normal")


# Slack COMMAND Handler: listen for help-slack-bolt
@bolt.command("/help-slack-bolt")
async def slash_help(ack, body, say):
    user_id = body["user_id"]
    await ack(f"Request for help has been sent <@{user_id}>!")

    # Check if the user is allowed to use the command
    if user_id in allowed_bot_users:
        # Respond to the command
        await say(f"Hello, <@{user_id}>")
    else:
        await say(f"Sorry, <@{user_id}>, you are not allowed to use this command.")


# Slack COMMAND Handler: listen for add-contact
@bolt.command("/add-contact")
async def add_contact(ack, respond, commandadd):
    # Acknowledge command request
    await ack()

    # Get user's ID from the command text
    user_id = await commandadd['text']

    provided_id_has_correct_format = re.match("^U[A-Z0-9]{8,}$", user_id)
    if provided_id_has_correct_format:
        # Add user to contacts
        my_contacts[user_id] = user_id
        # Respond with success message
        await respond(f"User {user_id} added to contacts.")
    else:
        await respond("Invalid format. Please provide a valid Slack User ID.")


# Slack COMMAND Handler: listen for get-contact
@bolt.command("/get-contact")
async def get_contact(ack, respond, commandget):
    # Acknowledge command request
    await ack()

    user_id = await commandget['text']
    if user_id in my_contacts:
        await respond(f"Contact found for User ID: {my_contacts[user_id]}")
    else:
        await respond(f"No contact found for User ID: {user_id}")


# Database Function
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


# starts the Socket Mode handler using the AsyncApp instance
async def main():
    handler = AsyncSocketModeHandler(bolt, os.environ["POETRY_SCM_XAPP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())

import datetime
import os
import re
import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from motor import motor_asyncio
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.fastapi import SlackRequestHandler


load_dotenv()  # read local .env file

app = App(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET")
)

fapi = FastAPI()

app_handler = SlackRequestHandler(app)

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


@fapi.post("/slack/events")
def endpoint(req: Request):
    """
    FastAPI endpoint receive Slack and process with SlackRequestHandler
    :param req:
    :return:
    """
    return app_handler.handle(req)


async def increase_counter(message_type: str):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d")

    current_data = await collection.find_one({"date": formatted_date})

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


@app.message(re.compile("(asap|help|urgent)", re.I))
def message_urgent(message, say):
    say(
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
    asyncio.create_task(increase_counter('urgent'))  # using asyncio.create_task to schedule the coroutine


@app.message(re.compile("(important|need|soon)", re.I))
def message_important(message, say):
    say(
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
    asyncio.create_task(increase_counter('important'))  # using asyncio.create_task to schedule the coroutine


@app.message(re.compile("(hi|hello|hey)", re.I))
def say_hello_regex(say, context):
    # regular expression matches are inside of context.matches
    greeting = context['matches'][0]
    say(f"{greeting}, how are you?")

    # TODO: get user_id from message
    user_id = "test"
    increase_counter_based_on_user_id(user_id=user_id)


def increase_counter_based_on_user_id(user_id: str):
    if user_id in contacts.keys():
        increase_counter("important")
    else:
        increase_counter("normal")


# Start app using WebSockets
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["POETRY_SCM_XAPP_TOKEN"])
    handler.start()
'''
# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
'''

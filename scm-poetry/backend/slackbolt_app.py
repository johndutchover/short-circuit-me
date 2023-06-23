import datetime
import os
import re

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from motor import motor_asyncio
from pydantic import BaseModel
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()  # read local .env file

app = App(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET")
)
app_handler = SlackRequestHandler(app)


# Define the data model Pydantic
class Item(BaseModel):
    msg_date: str
    count1: int
    flag: int
    count2: int
    count3: int


# MongoDB connection string
uri = os.environ.get("POETRY_MONGODB_URL")
# Set the Stable API version when creating a new client
client = motor_asyncio.AsyncIOMotorClient(os.environ["POETRY_MONGODB_URL"])
# database name in MongoDB
db = client["messagesdb"]
# collection name in MongoDB
collection = db["slackcoll"]

api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    """
    endpoint which handles incoming requests from Slack
    :param req:
    :return:
    """
    return await app_handler.handle(req)


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
        await collection.replace_one({"date": formatted_date}, new_data)
    else:
        print(f"{message_type} is not a valid key in the document")


@app.message(re.compile("(asap|help|urgent)", re.I))
async def message_urgent(message, say):
    """
    Increment counter of Priority 1 (urgent) string matches.
    Say() sends a message to the channel where the event was triggered.
    :param message: Message object
    :param say: Say function
    :return: None
    """
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
    await increase_counter('urgent')


@app.message(re.compile("(important|need|soon)", re.I))
async def message_important(message, say):
    """
    Increment counter of Priority 2 (important) string matches.
    Say() sends a message to the channel where the event was triggered.
    :param message: Message object
    :param say: Say function
    :return: None
    """
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
    await increase_counter('important')


@app.message(re.compile("(hi|hello|hey)", re.I))
async def say_hello_regex(say, context):
    # regular expression matches are inside of context.matches
    greeting = context['matches'][0]
    say(f"{greeting}, how are you?")
    await increase_counter('normal')


@app.action("button_click")
def action_button_click(body, ack, say):
    """
    Acknowledge the action.
    :param body: Action payload
    :param ack: Acknowledge function
    :param say: Say function
    :return: None
    """
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


# Start app using WebSockets
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["POETRY_SCM_XAPP_TOKEN"])
    handler.start()
'''
# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
'''

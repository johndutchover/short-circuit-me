import os
import re

from dotenv import load_dotenv
from slack_bolt import App
from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()  # read local .env file

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
    something to do with endpoint
    :param req:
    :return:
    """
    return await app_handler.handle(req)


counter = 0

str_help = r"(?:\bhelp\b)"
regex_help = re.compile(str_help, flags=re.I)


@app.message(regex_help)
def increase_notification_count():
    """
    increment counter of help strings
    :return:
    """
    global counter
    counter += 1

    print(counter)


# Add middleware / listeners here
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html

str_hello = r"(?:\bhello\b)"
regex_hello = re.compile(str_hello, flags=re.I)


@app.message(regex_hello)
def message_hello(message, say):
    """
    increment counter of help strings
    say() sends a message to the channel where the event was triggered
    :param message:
    :param say:
    :return:
    """
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

    print("Hello")


@app.event("message")
def handle_message_events(body, logger):
    """
    hangle Slack message events
    :param body:
    :param logger:
    :return:
    """
    logger.info(body)


@app.action("button_click")
def action_button_click(body, ack, say):
    """
    Acknowledge the action
    :param body:
    :param ack:
    :param say:
    :return:
    """
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


# Start app using WebSockets
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["POETRY_SCM_XAPP_TOKEN"]).start()

# Start the Bolt app
# if __name__ == "__main__":
#    app.start(port=3000)
#    app.start(port=int(os.environ.get("PORT", 3000)))

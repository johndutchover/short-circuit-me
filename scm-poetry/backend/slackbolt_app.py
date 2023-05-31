# https://api.slack.com/apps/A059F0MBC4Q
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# read local .env file
load_dotenv()

# Initializes your app with your bot token and socket mode handler
app = App(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    # signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET") # not required for socket mode
)


# Add middleware / listeners here


# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
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


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


# Start app using WebSockets
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["POETRY_SCM_XAPP_TOKEN"]).start()
    handler.start()

# development use
# if __name__ == "__main__":
#    slackboltapp.start(port=int(os.environ.get("PORT", 3000)))

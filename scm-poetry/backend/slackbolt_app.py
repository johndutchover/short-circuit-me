# https://api.slack.com/apps/A059F0MBC4Q
import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# load dotenv
load_dotenv()

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("POETRY_SCM_XOXB_TOKEN"))


# Initializes app-level (xapp) token and signing secret
# slackboltapp = App(
#    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
#    # signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET") # not required for socket mode
# )

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")


# Start app using WebSockets
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["POETRY_SCM_XAPP_TOKEN"]).start()

# development use
# if __name__ == "__main__":
#    slackboltapp.start(port=int(os.environ.get("PORT", 3000)))


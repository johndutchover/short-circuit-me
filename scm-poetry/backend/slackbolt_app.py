# https://api.slack.com/apps/A059F0MBC4Q
import os
# Use the package we installed
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes app-level (xapp) token and signing secret
slackboltapp = App(
    token=os.environ.get("POETRY_SCM_XOXB_TOKEN"),
    # signing_secret=os.environ.get("POETRY_SCM_BOT_SIGNINGSECRET") # not required for socket mode
)

# Add functionality here
# @app.event("app_home_opened") etc


# Request URLs (development use)
# if __name__ == "__main__":
#    slackboltapp.start(port=int(os.environ.get("PORT", 3000)))

# using WebSockets
if __name__ == "__main__":
    SocketModeHandler(App, os.environ["POETRY_SCM_XAPP_TOKEN"]).start()

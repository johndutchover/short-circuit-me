# https://api.slack.com/apps/A059F0MBC4Q
import os
# Use the package we installed
from slack_bolt import App

# Initializes app-level (xapp) token and signing secret
slackboltapp = App(
    token=os.environ.get("POETRY_SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("POETRY_SLACK_SIGNING_SECRET")
)

# Add functionality here
# @app.event("app_home_opened") etc


# Start your app
if __name__ == "__main__":
    slackboltapp.start(port=int(os.environ.get("PORT", 3000)))

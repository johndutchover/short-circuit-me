# https://api.slack.com/apps/A058DBF7NCQ
import os
# Use the package we installed
from slack_bolt import App

# Initializes your app with your bot token and signing secret
slackboltapp = App(
    token=os.environ.get("POETRY_SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("POETRY_SLACK_SIGNING_SECRET")
)

# Add functionality here
# @app.event("app_home_opened") etc


# Start your app
if __name__ == "__main__":
    slackboltapp.start(port=int(os.environ.get("PORT", 3000)))

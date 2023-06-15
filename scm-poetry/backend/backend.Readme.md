# Backend
Slack App: ShortCircuitMe

## Components

### FastAPI

### Slack | Bolt for Python
https://slack.dev/bolt-python/concepts

#### Socket Mode
https://api.slack.com/apis/connections/socket
Note: Apps using Socket Mode are not currently allowed in the public [Slack App Directory](https://slack.com/apps).
- created by calling the [apps.connections.open](https://api.slack.com/methods/apps.connections.open) method.

##### Behavior
- app connects to Slack via a WebSocket connection and receives data from Slack over the socket connection
- does **not** require exposing a public HTTP Request URL

##### Features
- allows your app to use the Slack [Events API](https://api.slack.com/apis/connections/events-api)

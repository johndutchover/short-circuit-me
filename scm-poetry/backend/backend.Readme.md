# Backend
Slack App: ShortCircuitMe

## Components

### FastAPI
- Endpoint for Slack events
  - [Events API](https://api.slack.com/apis/connections/events-api)

### MongoDB Atlas
- FastAPI connects to MongoDB using the [Motor (Async)](https://www.mongodb.com/docs/drivers/motor/) driver.

### Slack | Bolt for Python
App needs to be compatible with asyncio’s async/await programming model
- AsyncSocketModeHandler used to run AsyncApp

#### [Async version of Bolt](https://slack.dev/bolt-python/concepts#async)
- AsyncApp relies on [AIOHTTP](https://pypi.org/project/aiohttp/)

#### Bolt Adapters
- slack_bolt.adapter.socket_mode (PyPI: slack_sdk)
  - fastapi
  - socket_mode

##### Socket Mode
https://api.slack.com/apis/connections/socket

###### Method access
- created at _runtime_ by calling the [apps.connections.open](https://api.slack.com/methods/apps.connections.open) method.

```text
NOTE
Apps using Socket Mode are not currently allowed in the public [Slack App Directory](https://slack.com/apps).
```

##### Behavior
Slack will use a WebSocket URL to communicate with ShortCircuitMe
- Receives data from Slack over the socket connection.

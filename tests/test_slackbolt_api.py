# test_slackbolt_api.py

import pytest
from backend.slackbolt_api import message_urgent
import asyncio

@pytest.fixture
def mock_slack_client(mocker):
    return mocker.MagicMock()

@pytest.mark.asyncio
async def test_message_urgent(mock_slack_client):
    # Create a mock message event
    mock_message_event = {
        'user': 'USER_ID',
        'channel': 'CHANNEL_ID',
        'text': 'This is an urgent message!',
    }

    # Create a mock asynchronous result
    mock_result = asyncio.Future()
    mock_result.set_result(None)

    # Set the return value for the async function call
    mock_slack_client.chat_postEphemeral.return_value = mock_result

    # Call the message_urgent function with the mock event and client
    await message_urgent(mock_message_event, mock_slack_client)

    # Ensure that chat_postEphemeral is called on the mock Slack client
    mock_slack_client.chat_postEphemeral.assert_called_once()

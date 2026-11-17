from unittest.mock import Mock, patch

import requests

from api_client import fetch_users


def test_fetch_users_success():
    fake_users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]

    fake_response = Mock()
    fake_response.json.return_value = fake_users
    fake_response.raise_for_status.return_value = None

    with patch("api_client.requests.get", return_value=fake_response) as mock_get:
        result = fetch_users()

    assert result == fake_users
    mock_get.assert_called_once_with(
        "https://jsonplaceholder.typicode.com/users",
        timeout=10,
    )


def test_fetch_users_http_error():
    fake_response = Mock()
    fake_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Server Error"
    )

    with patch("api_client.requests.get", return_value=fake_response):
        result = fetch_users()

    assert result == []


def test_fetch_users_connection_error():
    with patch(
        "api_client.requests.get",
        side_effect=requests.exceptions.ConnectionError("Connection failed"),
    ):
        result = fetch_users()

    assert result == []


def test_fetch_users_invalid_json():
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.side_effect = requests.exceptions.JSONDecodeError(
        "Invalid JSON", "invalid", 0
    )

    with patch("api_client.requests.get", return_value=fake_response):
        result = fetch_users()

    assert result == []


def test_fetch_users_unexpected_data_format():
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {"users": []}

    with patch("api_client.requests.get", return_value=fake_response):
        result = fetch_users()

    assert result == []
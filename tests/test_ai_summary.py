from unittest.mock import Mock

from ai_summary import generate_ai_summary

from openai import OpenAIError


def test_generate_ai_summary_success():
    report = {
        "total_users": 2,
        "users": [
            {
                "id": 1,
                "name": "Alice",
                "email": "alice@example.com",
                "company": "Acme Ltd",
            },
            {
                "id": 2,
                "name": "Bob",
                "email": "bob@example.com",
                "company": "Beta Inc",
            },
        ],
    }

    fake_client = Mock()
    fake_client.responses.create.return_value.output_text = (
        "The directory contains 2 users from 2 companies."
    )

    result = generate_ai_summary(report, client=fake_client)

    assert result == "The directory contains 2 users from 2 companies."
    fake_client.responses.create.assert_called_once()


def test_generate_ai_summary_empty_report():
    report = {
        "total_users": 0,
        "users": [],
    }

    fake_client = Mock()

    result = generate_ai_summary(report, client=fake_client)

    assert result is None
    fake_client.responses.create.assert_not_called()


def test_ai_prompt_excludes_personal_information():
    report = {
        "total_users": 1,
        "users": [
            {
                "id": 1,
                "name": "Alice Smith",
                "email": "alice@example.com",
                "company": "Acme Ltd",
            }
        ],
    }

    fake_client = Mock()
    fake_client.responses.create.return_value.output_text = (
        "One user from Acme Ltd."
    )

    generate_ai_summary(report, client=fake_client)

    call_kwargs = fake_client.responses.create.call_args.kwargs
    prompt = call_kwargs["input"]

    assert "Alice Smith" not in prompt
    assert "alice@example.com" not in prompt

    assert "Acme Ltd" in prompt
    assert '"total_users": 1' in prompt
    assert '"total_companies": 1' in prompt


def test_generate_ai_summary_api_failure(caplog):
    report = {
        "total_users": 1,
        "users": [
            {
                "id": 1,
                "name": "Alice",
                "email": "alice@example.com",
                "company": "Acme Ltd",
            }
        ],
    }

    fake_client = Mock()

    fake_client.responses.create.side_effect = OpenAIError(
        "Simulated AI service failure"
    )

    result = generate_ai_summary(report, client=fake_client)

    assert result is None
    fake_client.responses.create.assert_called_once()
    assert "AI summary generation failed" in caplog.text
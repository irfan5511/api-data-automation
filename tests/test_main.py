from unittest.mock import patch

import main


def test_main_with_ai_enabled(capsys):
    fake_users = [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "company": {"name": "Acme Ltd"},
        }
    ]

    fake_summary = "The directory contains one user from Acme Ltd."

    with (
        patch("main.ENABLE_AI_SUMMARY", True),
        patch("main.fetch_users", return_value=fake_users),
        patch("main.save_user_report") as mock_save,
        patch("main.generate_ai_summary", return_value=fake_summary) as mock_ai,
    ):
        mock_save.return_value = "reports/users_report.json"

        main.main()

    captured = capsys.readouterr()

    assert "Total users: 1" in captured.out
    assert "AI Business Summary:" in captured.out
    assert fake_summary in captured.out

    mock_ai.assert_called_once()
    mock_save.assert_called_once()


def test_main_with_ai_disabled(capsys):
    fake_users = [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "company": {"name": "Acme Ltd"},
        }
    ]

    with (
        patch("main.ENABLE_AI_SUMMARY", False),
        patch("main.fetch_users", return_value=fake_users),
        patch("main.save_user_report") as mock_save,
        patch("main.generate_ai_summary") as mock_ai,
    ):
        mock_save.return_value = "reports/users_report.json"

        main.main()

    captured = capsys.readouterr()

    assert "Total users: 1" in captured.out
    assert "Report saved to: reports/users_report.json" in captured.out
    assert "AI Business Summary:" not in captured.out

    mock_save.assert_called_once()
    mock_ai.assert_not_called()


def test_main_ai_summary_failure(capsys):
    fake_users = [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "company": {"name": "Acme Ltd"},
        }
    ]

    with (
        patch("main.ENABLE_AI_SUMMARY", True),
        patch("main.fetch_users", return_value=fake_users),
        patch("main.save_user_report") as mock_save,
        patch("main.generate_ai_summary", return_value=None) as mock_ai,
    ):
        mock_save.return_value = "reports/users_report.json"

        main.main()

    captured = capsys.readouterr()

    assert "Total users: 1" in captured.out
    assert "Report saved to: reports/users_report.json" in captured.out

    assert "AI Business Summary:" not in captured.out

    mock_save.assert_called_once()
    mock_ai.assert_called_once()
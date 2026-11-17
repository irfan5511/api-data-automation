import json

from report_generator import generate_user_report, save_user_report


def test_generate_user_report():
    users = [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "company": {"name": "Acme Ltd"},
        },
        {
            "id": 2,
            "name": "Bob",
            "email": "bob@example.com",
        },
    ]

    report = generate_user_report(users)

    assert report["total_users"] == 2
    assert report["users"][0]["name"] == "Alice"
    assert report["users"][0]["company"] == "Acme Ltd"
    assert report["users"][1]["company"] == "Unknown"


def test_generate_empty_user_report():
    report = generate_user_report([])

    assert report["total_users"] == 0
    assert report["users"] == []


def test_save_user_report(tmp_path):
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

    output_file = tmp_path / "reports" / "users_report.json"

    saved_path = save_user_report(report, output_file)

    assert saved_path == output_file
    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8") as file:
        saved_report = json.load(file)

    assert saved_report == report
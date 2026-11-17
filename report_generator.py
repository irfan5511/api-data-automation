import json
from pathlib import Path


def generate_user_report(users):
    return {
        "total_users": len(users),
        "users": [
            {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "company": user.get("company", {}).get("name", "Unknown"),
            }
            for user in users
        ],
    }


def save_user_report(report, filename="reports/users_report.json"):
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return output_path
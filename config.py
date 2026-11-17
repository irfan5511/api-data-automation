import os

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://jsonplaceholder.typicode.com"
)

API_TIMEOUT = float(os.getenv("API_TIMEOUT", "10"))

REPORT_PATH = os.getenv(
    "REPORT_PATH",
    "reports/users_report.json"
)

ENABLE_AI_SUMMARY = (
    os.getenv("ENABLE_AI_SUMMARY", "false").lower() == "true"
)
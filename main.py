import logging

from ai_summary import generate_ai_summary
from api_client import fetch_users
from config import ENABLE_AI_SUMMARY, REPORT_PATH
from report_generator import generate_user_report, save_user_report


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting API data automation")

    users = fetch_users()

    if not users:
        logger.warning("No users available. Report not generated.")
        return

    report = generate_user_report(users)
    output_path = save_user_report(report, REPORT_PATH)

    logger.info("Report saved to %s", output_path)

    print(f"Total users: {report['total_users']}")
    print(f"Report saved to: {output_path}")

    if ENABLE_AI_SUMMARY:
        logger.info("AI summary generation enabled")

        summary = generate_ai_summary(report)

        if summary:
            print("\nAI Business Summary:")
            print(summary)
        else:
            logger.warning("AI summary unavailable")
    else:
        logger.info("AI summary generation disabled")


if __name__ == "__main__":
    main()
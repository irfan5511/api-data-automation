import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

logger = logging.getLogger(__name__)


def generate_ai_summary(report, client=None):
    if not report.get("users"):
        logger.warning("No user data available for AI analysis")
        return None

    if client is None:
        if not os.getenv("OPENAI_API_KEY"):
            logger.warning("OPENAI_API_KEY is missing. Skipping AI summary.")
            return None

        client = OpenAI(timeout=20.0, max_retries=1)

    model = os.getenv("AI_MODEL", "gpt-5.5")

    company_names = [
        user["company"]
        for user in report["users"]
        if isinstance(user.get("company"), str)
    ]

    ai_data = {
        "total_users": report["total_users"],
        "companies": sorted(set(company_names)),
        "total_companies": len(set(company_names)),
    }

    prompt = (
        "Analyze this user directory report.\n"
        "Provide a brief business-friendly summary covering:\n"
        "1. Total users\n"
        "2. Companies represented\n"
        "3. Useful observations supported by the data\n\n"
        "Do not invent facts or make unsupported conclusions.\n\n"
        f"Report:\n{json.dumps(ai_data, indent=2)}"
    )

    try:
        response = client.responses.create(
            model=model,
            instructions=(
                "You are a business reporting assistant. "
                "Use only the supplied data. "
                "Write clearly and concisely."
            ),
            input=prompt,
        )

        summary = response.output_text.strip()

        if not summary:
            logger.warning("AI returned an empty summary")
            return None

        logger.info("AI summary generated successfully")
        return summary

    except OpenAIError as error:
        logger.error("AI summary generation failed: %s", error)
        return None
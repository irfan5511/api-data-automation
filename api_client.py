import logging

import requests

from config import API_BASE_URL, API_TIMEOUT

logger = logging.getLogger(__name__)

BASE_URL = "https://jsonplaceholder.typicode.com"


def fetch_users():
    url = f"{API_BASE_URL}/users"

    try:
        logger.info("Fetching users from API")

        response = requests.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()

        users = response.json()

        if not isinstance(users, list):
            raise ValueError("API returned an unexpected data format")

        logger.info("Successfully fetched %s users", len(users))
        return users

    except requests.exceptions.RequestException as error:
        logger.error("API request failed: %s", error)
        return []

    except ValueError as error:
        logger.error("Invalid API response: %s", error)
        return []
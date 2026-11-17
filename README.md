# API Data Automation with AI Integration

A Python automation application that retrieves data from a REST API, generates structured JSON reports, and optionally produces AI-powered business summaries.

The project demonstrates API integration, automated reporting, error handling, logging, configuration management, AI integration, and automated testing.

## Features

- Fetch user data from a public REST API.
- Validate API responses and handle network errors.
- Generate structured JSON business reports.
- Configure API settings using environment variables.
- Record application events using Python logging.
- Generate optional AI-powered summaries using the OpenAI API.
- Minimize personal information sent to AI services.
- Handle AI service failures without interrupting normal reporting.
- Test API and AI workflows using mocked responses.

## Project Structure

```text
api-data-automation/
├── tests/
│   ├── test_ai_summary.py
│   ├── test_api_clients.py
│   ├── test_main.py
│   └── test_report_generator.py
├── ai_summary.py
├── api_client.py
├── config.py
├── main.py
├── report_generator.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

The application creates the `reports/` directory when generating reports.

## Requirements

- Python 3.10 or later
- pip
- Internet access for live API requests
- OpenAI API credentials and available credits only for optional live AI summaries

## Installation

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Create a private `.env` file using `.env.example` as a reference.

Example configuration:

```dotenv
OPENAI_API_KEY=your_api_key_here
AI_MODEL=your_available_model
```

Never commit real credentials to GitHub.

Additional environment variables:

| Variable | Purpose | Default |
|---|---|---|
| `API_BASE_URL` | REST API base URL | `https://jsonplaceholder.typicode.com` |
| `API_TIMEOUT` | Request timeout in seconds | `10` |
| `REPORT_PATH` | JSON report destination | `reports/users_report.json` |
| `ENABLE_AI_SUMMARY` | Enable optional AI generation | `false` |
| `AI_MODEL` | OpenAI model identifier | Configured in `ai_summary.py` |

## Running the Application

Generate a normal JSON report:

```bash
python main.py
```

Generate a report at a custom location:

```bash
REPORT_PATH=reports/custom_users.json python main.py
```

Enable AI summary generation:

```bash
ENABLE_AI_SUMMARY=true python main.py
```

Live AI requests require a valid API key, model access, and available API credits. API usage may incur charges.

If AI generation fails, the application logs the error while preserving the standard JSON report.

## JSON Report

The application retrieves sample user data from JSONPlaceholder and creates `reports/users_report.json`.

Example structure:

```json
{
  "total_users": 1,
  "users": [
    {
      "id": 1,
      "name": "Alice",
      "email": "alice@example.com",
      "company": "Acme Ltd"
    }
  ]
}
```

The example above illustrates the output schema.

## AI Integration

AI summaries use aggregated company information, including user counts and distinct company names.

Individual user names and email addresses are excluded from AI prompts.

The AI feature is disabled by default and can be tested using mocked responses without consuming API credits.

## Automated Testing

Run all tests:

```bash
python -m pytest -v
```

The test suite covers API responses, network failures, JSON reporting, AI-enabled and disabled workflows, AI errors, and AI prompt privacy.

Latest development result: **15 tests passed**.

## Technologies

Python, requests, OpenAI Python SDK, python-dotenv, pytest, JSON, logging, and Git.

## Status

Core API automation and optional AI integration implemented. Automated tests passing. Live AI request handling verified.
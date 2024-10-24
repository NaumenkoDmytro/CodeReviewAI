# Automated Code Review Tool
This project is a backend service designed to automate code reviews by integrating with GitHub and OpenAI's GPT API. It utilizes FastAPI for asynchronous API operations, Redis for caching, and Docker for containerization.

## Features
* Fetches and processes files from a GitHub repository.
* Uses OpenAI's GPT API to analyze code.
* Caches requests to improve performance.
* Asynchronous operations with FastAPI.
* Docker and Docker Compose setup for easy environment management.
* Supports Redis caching for efficient API call management.

## Setup
### Prerequisites
* Docker and Docker Compose installed.
* OpenAI API key and GitHub API token.
* Python 3.x installed locally if running without Docker.
* Redis installed locally or use the Docker container.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/NaumenkoDmytro/CodeReviewAI.git
cd CodeReviewAI
```
2. Create a `.env` file based on the `app/env_example` file and add your credentials:
```bash
cp app/env_example .env
```
3. Update the `.env` file with your OpenAI API key and GitHub token:
```env
OPENAI_API_KEY=your-openai-api-key
GITHUB_API_TOKEN=your-github-token
```

### Launch

This project is supposed to be built in docker, so after the installation steps, you need to run the following:
```bash
docker-compose build
docker-compose up -d
```

The service should now be accessible at `http://localhost:8000`

### Tests

For tests you need to run the following:
```bash
docker-compose exec web poetry run pytest --cov=app --cov-report=term-missing
```


## Scaling ideas (Part2)
Handling Large Repositories: For large repositories, you can paginate the GitHub API results and review them in chunks. Use GitHub's pagination mechanism (using Link headers).
Handling Large Volumes of Requests: Use task queues like Celery for processing reviews asynchronously and Redis as a message broker. This will help to offload long-running reviews and allow scaling.
OpenAI API Limits: For large repositories, you may split the repository's content into multiple OpenAI requests and combine the results. Respect rate limits by implementing retry logic and exponential backoff.

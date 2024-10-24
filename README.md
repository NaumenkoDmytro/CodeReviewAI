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
* Docker and Docker Compose installed.
* OpenAI API key and GitHub API token.
* Python 3.x installed locally if running without Docker.
* Redis installed locally or use the Docker container.

## Installation

1. Clone the repository:
```bash
`git clone https://github.com/NaumenkoDmytro/CodeReviewAI.git`
`cd CodeReviewAI`

2. Create a `.env` file based on the `app/env_example` file and add your credentials:
```env
`cp app/env_example .env`


3. Update the `.env` file with your OpenAI API key and GitHub token:
```bash
`OPENAI_API_KEY=your-openai-api-key`
`GITHUB_API_TOKEN=your-github-token`



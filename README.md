<<<<<<< HEAD
# llm-log-analyzer
LLM-powered CI/CD failure analyzer using FastAPI, Docker , Jenkins, and Ollama for automated log debugging.
=======
# LLM Log Analyzer

A FastAPI backend that analyzes CI/CD logs and returns a failure summary, root cause, and fix suggestion.

## Features
- FastAPI backend
- Swagger UI at `/docs`
- JSON log analysis endpoint
- Raw text log analysis endpoint
- Optional LLM-powered analysis using OpenAI Responses API
- Jenkins pipeline integration
- Docker support

## Tech Stack
- Python
- FastAPI
- Uvicorn
- OpenAI SDK
- Jenkins
- Docker

## Setup

### 1. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
>>>>>>> 8902d62 (LLM CI/CD analyzer with Docker)

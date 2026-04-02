# LLM-Powered CI/CD Failure Analyzer

A FastAPI-based backend service that analyzes CI/CD logs and generates failure summaries, root causes, and suggested fixes using a local LLM (Ollama).

---

##  Features

- FastAPI backend with Swagger UI (`/docs`)
- CI/CD log analysis via REST APIs
- Local LLM integration using Ollama (no external API cost)
- Heuristic fallback for reliability
- Dockerized for consistent deployment
- Jenkins pipeline defined for CI/CD automation

---

## Architecture

Jenkins → Docker → FastAPI → Ollama

Flow:
1. CI/CD pipeline generates logs  
2. Logs are sent to FastAPI API  
3. Backend sends logs to Ollama  
4. Returns structured analysis  

---

##  Tech Stack

- Python  
- FastAPI  
- Uvicorn  
- Ollama (Local LLM)  
- Docker  
- Jenkins (Pipeline defined)  
- Pytest  

---

##  Project Structure

app/  
jenkins/  
tests/  
Dockerfile  
requirements.txt  
README.md  

---

##  Setup (Local)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama run gemma3
uvicorn app.main:app --reload
Open:
http://127.0.0.1:8000/docs

##  API Usage

curl -X POST http://127.0.0.1:8000/analyze
-H "Content-Type: application/json"
-d '{"log_text":"ERROR: No module named requests"}'

Example Response:


{
"status": "failure",
"summary": "Module 'requests' not found",
"root_cause": "Missing dependency",
"suggestion": "Install the required package",
"confidence": 0.95,
"provider": "llm"
}

##  Docker


docker build -t llm-log-analyzer .

docker run -p 8000:8000
-e OLLAMA_HOST=http://host.docker.internal:11434

-e OLLAMA_MODEL=gemma3
llm-log-analyzer

## ⚙️ Jenkins (Planned)

- Build Docker image  
- Run container  
- Call API  
- Print results  

---

## 💡 Key Highlights

- Automates CI/CD debugging  
- Works offline using local LLM  
- Demonstrates DevOps + AI integration  
- Containerized for portability  

---

##  Author

Adabala Jishnu Preethi
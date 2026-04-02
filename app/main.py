from fastapi import Body, FastAPI

from app.llm_service import analyze_log
from app.schemas import AnalysisResult, LogInput

app = FastAPI(
    title="LLM Log Analyzer",
    version="1.0.0",
    description="A FastAPI app that analyzes CI/CD logs using heuristic rules and optional LLM support.",
)


@app.get("/")
def home():
    return {
        "message": "LLM Log Analyzer is running",
        "docs": "/docs",
        "health": "/health",
        "analyze_json": "/analyze",
        "analyze_raw": "/analyze-raw",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResult)
def analyze(payload: LogInput):
    return analyze_log(payload.log_text)


@app.post("/analyze-raw", response_model=AnalysisResult)
def analyze_raw(log_text: str = Body(..., media_type="text/plain")):
    return analyze_log(log_text)
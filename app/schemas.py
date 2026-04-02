from typing import Literal

from pydantic import BaseModel, Field


class LogInput(BaseModel):
    log_text: str = Field(..., min_length=1, max_length=50_000)


class AnalysisResult(BaseModel):
    status: Literal["success", "failure", "unknown"]
    summary: str
    root_cause: str
    suggestion: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    provider: Literal["llm", "heuristic"]
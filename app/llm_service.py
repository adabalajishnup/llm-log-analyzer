import json
import os
import re
from typing import Any, Dict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3")


def _clean_json_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _extract_json(text: str) -> Dict[str, Any]:
    text = _clean_json_text(text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return {}
    return {}


def _heuristic_analysis(log_text: str) -> Dict[str, Any]:
    text = log_text.lower()

    result = {
        "status": "success",
        "summary": "No obvious failure keywords were found in the log.",
        "root_cause": "No clear root cause detected from the provided text.",
        "suggestion": "The pipeline looks healthy. If this is unexpected, inspect the full console output.",
        "confidence": 0.55,
        "provider": "heuristic",
    }

    if any(keyword in text for keyword in ["error", "failed", "exception", "traceback", "fatal", "cannot", "could not"]):
        result["status"] = "failure"
        result["summary"] = "The pipeline contains failure-related log messages."
        result["confidence"] = 0.78

        if "module not found" in text or "no module named" in text:
            result["root_cause"] = "A Python dependency is missing."
            result["suggestion"] = "Install the missing package and verify the requirements file."
        elif "permission denied" in text:
            result["root_cause"] = "The process does not have enough permissions."
            result["suggestion"] = "Check file permissions, Jenkins credentials, and execution rights."
        elif "connection refused" in text or "timeout" in text:
            result["root_cause"] = "A network or service dependency is unavailable."
            result["suggestion"] = "Check service availability, URLs, and network access."
        elif "syntaxerror" in text:
            result["root_cause"] = "There is a syntax issue in the code."
            result["suggestion"] = "Inspect the line number mentioned in the stack trace."
        else:
            result["root_cause"] = "The log indicates a build or runtime failure."
            result["suggestion"] = "Check the first error line, recent code changes, and dependency setup."

    return result


def _normalize_result(data: Dict[str, Any], fallback: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(fallback)

    if isinstance(data, dict):
        for key in ["status", "summary", "root_cause", "suggestion", "confidence"]:
            if key in data and data[key] not in (None, ""):
                result[key] = data[key]

    if result["status"] not in ["success", "failure", "unknown"]:
        result["status"] = "unknown"

    try:
        result["confidence"] = float(result["confidence"])
    except Exception:
        result["confidence"] = float(fallback["confidence"])

    result["confidence"] = max(0.0, min(1.0, result["confidence"]))
    return result


def analyze_log(log_text: str) -> Dict[str, Any]:
    fallback = _heuristic_analysis(log_text)

    prompt = f"""
Analyze this CI/CD log and return ONLY valid JSON.

Required keys:
- status: success, failure, or unknown
- summary: short explanation
- root_cause: likely cause
- suggestion: practical fix
- confidence: number from 0 to 1

Log:
{log_text}
""".strip()

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "system": "You are a senior DevOps assistant. Return only JSON.",
        "format": "json",
        "stream": False,
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = Request(
            f"{OLLAMA_HOST}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(req, timeout=120) as resp:
            raw = json.loads(resp.read().decode("utf-8"))

        response_text = raw.get("response", "")
        parsed = _extract_json(response_text)
        normalized = _normalize_result(parsed, fallback)
        normalized["provider"] = "llm"
        return normalized

    except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as e:
        print("OLLAMA ERROR:", repr(e))
        return fallback
    except Exception as e:
        print("OLLAMA ERROR:", repr(e))
        return fallback
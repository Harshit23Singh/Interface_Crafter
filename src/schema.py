from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SimplificationRequest:
    text: str
    user_prompt: str = ""


@dataclass
class SimplificationResponse:
    summary: str
    key_points: List[str]
    obligations: List[str]
    risks: List[str]
    actions: List[str]
    disclaimers: List[str]
    raw_model_output: Optional[str] = None


def load_json_safely(text: str) -> Optional[Dict[str, Any]]:
    try:
        import orjson as _json
        return _json.loads(text)
    except Exception:
        try:
            import json as _json2
            return _json2.loads(text)
        except Exception:
            return None


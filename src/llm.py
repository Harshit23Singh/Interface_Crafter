import os
from typing import List

from .schema import SimplificationRequest, SimplificationResponse, load_json_safely


SYSTEM_PROMPT = (
    "You are a legal document simplifier. Convert complex legal text into clear, neutral, and accessible guidance for laypeople. "
    "Avoid legalese. Use plain English. Do not provide legal advice; provide information and potential actions. "
    "Output a strict JSON object with keys: summary, key_points, obligations, risks, actions, disclaimers."
)

USER_PROMPT_TEMPLATE = (
    "Document:\n\n{doc}\n\n"
    "Optional user context or questions:\n{user_prompt}\n\n"
    "Return ONLY JSON in this structure:\n"
    "{\n"
    "  \"summary\": string,\n"
    "  \"key_points\": string[],\n"
    "  \"obligations\": string[],\n"
    "  \"risks\": string[],\n"
    "  \"actions\": string[],\n"
    "  \"disclaimers\": string[]\n"
    "}\n"
)


def _fallback_simplify(req: SimplificationRequest) -> SimplificationResponse:
    text = req.text.strip()
    snippet = text[:500].replace("\n", " ")
    summary = (
        f"This document appears to be a legal text. Key content includes: '{snippet}'... "
        "This is an automated, non-legal summary."
    )
    return SimplificationResponse(
        summary=summary,
        key_points=["Important clauses may define obligations, rights, deadlines, and remedies."],
        obligations=["Review defined duties, timelines, and required approvals."],
        risks=["Non-compliance, fees, termination, or disputes may arise."],
        actions=["Clarify ambiguous terms", "Check dates and termination clauses", "Seek professional advice if needed"],
        disclaimers=["This is not legal advice.", "Consult a qualified attorney for your specific situation."],
        raw_model_output=None,
    )


def generate_guidance(req: SimplificationRequest) -> SimplificationResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback_simplify(req)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        user_prompt = USER_PROMPT_TEMPLATE.format(doc=req.text, user_prompt=req.user_prompt or "(none)")
        chat = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        content = chat.choices[0].message.content if chat.choices else ""
        parsed = load_json_safely(content) or {}

        def _get_list(key: str) -> List[str]:
            val = parsed.get(key)
            if isinstance(val, list):
                return [str(x) for x in val][:20]
            if isinstance(val, str) and val.strip():
                return [val.strip()]
            return []

        return SimplificationResponse(
            summary=str(parsed.get("summary") or "No summary produced."),
            key_points=_get_list("key_points"),
            obligations=_get_list("obligations"),
            risks=_get_list("risks"),
            actions=_get_list("actions"),
            disclaimers=_get_list("disclaimers") or ["This is not legal advice."],
            raw_model_output=content,
        )
    except Exception:
        return _fallback_simplify(req)


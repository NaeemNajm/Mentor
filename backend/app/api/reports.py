from fastapi import APIRouter
from ..core.config import settings
from ..db import engine
from sqlmodel import Session, select
from ..models import Block
from pydantic import BaseModel

router = APIRouter()

class ReportRequest(BaseModel):
    user_id: str

@router.post("/daily")
def daily_report(req: ReportRequest):
    # Simple rule-based summary. If OPENAI_API_KEY is set, this will attempt to call OpenAI.
    with Session(engine) as session:
        blocks = session.exec(select(Block).where(Block.user_id == req.user_id)).all()
    total = len(blocks)
    completed = sum(1 for b in blocks if b.completed)
    summary = {
        "total_blocks": total,
        "completed_blocks": completed,
        "completion_rate": f"{(completed/total*100) if total else 0:.1f}%",
        "insights": []
    }
    # If OPENAI_API_KEY is not provided, return rule-based summary
    if not settings.OPENAI_API_KEY:
        summary["insights"].append("Set OPENAI_API_KEY to enable AI-generated insights.")
        return summary

    # Minimal OpenAI call (optional)
    try:
        import requests
        prompt = f"User {req.user_id} completed {completed} of {total} blocks. Suggest 3 improvement tips."
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}", "Content-Type": "application/json"},
            json={"model": "gpt-4o-mini","messages":[{"role":"user","content":prompt}], "max_tokens": 200}
        )
        if resp.status_code == 200:
            j = resp.json()
            text = j["choices"][0]["message"]["content"] if j.get("choices") else resp.text
            summary["insights"].append(text)
        else:
            summary["insights"].append("OpenAI request failed; see logs")
    except Exception as e:
        summary["insights"].append(f"AI error: {e}")

    return summary

"""FastAPI microservice that processes AI prompts (stub)."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Service", version="0.1.0")

class AskPayload(BaseModel):
    prompt: str
    project_id: int | None = None
    user: str | None = None

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/ask")
async def ask(payload: AskPayload) -> dict:
    # Stubbed logic – replace with real model/provider calls later
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    answer = f"[echo] You said: {payload.prompt}"
    return {
        "answer": answer,
        "project_id": payload.project_id,
        "user": payload.user,
    }

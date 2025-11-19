"""FastAPI microservice that processes AI prompts (stub)."""
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

import openai

# Load environment variables from .env if present
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # or any other model you prefer

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

app = FastAPI(title="AI Service")

class AskPayload(BaseModel):
    """Incoming payload from Django assistant service."""
    prompt: str
    project_id: Optional[int] = None
    user: Optional[str] = None


class AskResponse(BaseModel):
    """Outgoing response to Django assistant service."""
    answer: str
    project_id: Optional[int] = None
    user: Optional[str] = None


@app.get("/health")
def health() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok"}


def generate_answer_with_openai(prompt: str, user: Optional[str] = None) -> str:
    """
    Generate answer using OpenAI Chat Completion.
    If something goes wrong, raise HTTPException.
    """
    try:
        # Basic single-message chat; in step 10 we will extend this with history.
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for a web project management tool.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            user=user,
        )
        return response.choices[0].message["content"].strip()
    except Exception as exc:
        # In production, you would log this
        raise HTTPException(status_code=502, detail=f"OpenAI error: {exc}")


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskPayload):
    """
    Main entry point:
    - If OPENAI_API_KEY is set -> use OpenAI
    - Otherwise -> simple echo fallback
    """
    prompt = payload.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    # If OpenAI is configured, use it
    if OPENAI_API_KEY:
        answer = generate_answer_with_openai(prompt, user=payload.user)
    else:
        # Fallback: echo behavior
        answer = f"[echo] You said: {prompt}"

    return AskResponse(
        answer=answer,
        project_id=payload.project_id,
        user=payload.user,
    )


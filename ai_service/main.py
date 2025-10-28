from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="AI Microservice")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "AI microservice"}

@app.post("/generate/")
def generate_response(prompt: str):
    # Позже сюда добавим реальный вызов LLM или OpenAI API
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    return {"response": f"AI response to: {prompt}"}
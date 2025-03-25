from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class Message(BaseModel):
    text: str

# Use environment variable to protect API key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.post("/api/chat")
async def chat(message: Message):
    if not DEEPSEEK_API_KEY:
        return {"error": "API key is missing. Set DEEPSEEK_API_KEY in environment variables."}

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={"model": "deepseek-chat", "messages": [{"role": "user", "content": message.text}]}
    )

    try:
        return {"response": response.json()["choices"][0]["message"]["content"]}
    except KeyError:
        return {"error": "Invalid API response. Check your DeepSeek API key and usage limits."}

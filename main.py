from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os  # Required for environment variables

app = FastAPI()

class Message(BaseModel):
    text: str

# Use environment variable (set in Vercel)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Critical! Replace "YOUR_DEEPSEEK_API_KEY"

@app.post("/api/chat")  # Changed from "/chat" to "/api/chat" to match your CURL test
async def chat(message: Message):
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": message.text}]
        }
    )
    return {"response": response.json()["choices"][0]["message"]["content"]}

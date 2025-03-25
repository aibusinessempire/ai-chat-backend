from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class Message(BaseModel):
    text: str

DEEPSEEK_API_KEY = "sk-af6e1672921341f7b36a004fa3d508b5"

@app.post("/api/chat")
async def chat(message: Message):
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
        json={"model": "deepseek-chat", "messages": [{"role": "user", "content": message.text}]}
    )
    return {"response": response.json()["choices"][0]["message"]["content"]}

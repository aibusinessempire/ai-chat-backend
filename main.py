from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from typing import Dict, Any

app = FastAPI(title="DeepSeek Chat API", version="1.0")

class Message(BaseModel):
    text: str

# Environment variable (set in Vercel/Railway)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.post("/api/chat")
async def chat(message: Message) -> Dict[str, Any]:
    """
    Process user message with DeepSeek AI.
    Returns:
        - AI response (success)
        - Error message (failure)
    """
    # Validate API key
    if not DEEPSEEK_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server error: DEEPSEEK_API_KEY not configured"
        )

    try:
        # Call DeepSeek API
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": message.text}]
            },
            timeout=10  # Prevents hanging requests
        )
        response.raise_for_status()  # Raises HTTPError for bad responses

        # Parse response
        data = response.json()
        return {
            "response": data["choices"][0]["message"]["content"],
            "usage": data.get("usage", {})
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"DeepSeek API error: {str(e)}"
        )
    except (KeyError, IndexError):
        raise HTTPException(
            status_code=502,
            detail="Invalid DeepSeek API response format"
        )

from fastapi import FastAPI
   from pydantic import BaseModel
   import requests

   app = FastAPI()

   class Message(BaseModel):
       text: str

   DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY"  # 🔑 Replace later!

   @app.post("/chat")
   async def chat(message: Message):
       response = requests.post(
           "https://api.deepseek.com/v1/chat/completions",
           headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
           json={"model": "deepseek-chat", "messages": [{"role": "user", "content": message.text}]}
       )
       return {"response": response.json()["choices"][0]["message"]["content"]}

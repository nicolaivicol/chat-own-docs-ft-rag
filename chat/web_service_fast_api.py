from fastapi import FastAPI, Form

from chat.chatobj import Chat
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins (you can customize this as needed).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify a list of allowed origins here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(data: dict):
    message = data.get('message')
    answer = chat.ask_gpt(message)
    docs = chat.get_titles_most_relevant_docs()
    return {
        "text": answer,
        "options": docs,
        "optionType": "radio"
    }


@app.get("/hi")
async def hi():
    return {"message": "Hello World"}


if __name__ == "__main__":
    chat = Chat()
    uvicorn.run(app, host="0.0.0.0", port=8000)

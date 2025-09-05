from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.chat import router as chat_router

app = FastAPI(title="Chatbot Take-Home API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

# Local dev: uvicorn app.main:app --reload --port 8787

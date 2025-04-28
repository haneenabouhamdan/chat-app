import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoints import message, user, auth

app = FastAPI(
    title="Chat App API",
    description="API for sending and retrieving messages between users.",
    version="1.0.0"
)


# Enable CORS for local development or frontend consumption
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Auth"])
app.include_router(message.router, tags=["Messages"])
app.include_router(user.router, tags=["Users"])

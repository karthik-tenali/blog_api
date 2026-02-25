# hello this is a comment
from fastapi import FastAPI, Request
import socket
import os

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "FastAPI running from WSL",
        "hostname": socket.gethostname(),
        "cwd": os.getcwd()
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/echo")
async def echo(q: str):
    return {"you_sent": q}

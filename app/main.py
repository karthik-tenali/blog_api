from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG
)


@app.get("/health")
async def health_check():
    return {"status": "Healthy"}
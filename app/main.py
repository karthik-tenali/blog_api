from fastapi import FastAPI
from app.config import settings
from app.api.v1.auth import router as auth_router

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=['auth'])

@app.get("/health")
async def health_check():
    return {"status": "Healthy"}
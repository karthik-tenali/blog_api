from fastapi import FastAPI
from app.config import settings
from app.api.v1.auth import router as auth_router
from contextlib import asynccontextmanager
from app.db.session import engine

@asynccontextmanager
async def life_span(app: FastAPI):
    print('Application Started')
    yield
    await engine.dispose()
    print('Application Stopped')

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
    lifespan=life_span
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=['auth'])

@app.get("/health")
async def health_check():
    return {"status": "Healthy"}
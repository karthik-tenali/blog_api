from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as user_router
from contextlib import asynccontextmanager
from app.db.session import engine, get_db
from app.middleware.logging import log_requests
from sqlalchemy.ext.asyncio import AsyncSession


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

class LimitBodySizeMiddleware(BaseHTTPMiddleware):
    MAX_BODY_SIZE = 10 * 1024 * 1024  # 10MB

    async def dispatch(self, request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_BODY_SIZE:
            return JSONResponse({"detail": "Request body too large"}, status_code=413)
        return await call_next(request)

app.add_middleware(LimitBodySizeMiddleware)

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    return await log_requests(request, call_next)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=['auth'])
app.include_router(user_router, prefix="/api/v1/users", tags=['users'])

@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    checks = {}
    
    try: 
        await db.execute(text("SELECT 1"))
        checks['database'] = 'healthy'
    except Exception:
        checks['database'] = 'unhealthy'
        
    overall = "healthy" if checks["database"] == "healthy" else "degraded"
    status_code = 200 if overall == "healthy" else 503    
    
    return JSONResponse(
        {
            "status" : overall,
            "checks" : checks
        },
        status_code= status_code
    )
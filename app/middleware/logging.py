import uuid, time, logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def log_requests(request :Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start = time.perf_counter()

    logger.info(
        "[%s] %s %s started",
        request_id,
        request.method,
        request.url.path,
    )

    response = await call_next(request)
    
    duration_ms = (time.perf_counter() - start) * 1000
    
    logger.info(
        "[%s] %s %s -> %s in %.2fms",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    
    response.headers["X-Request-ID"] = request_id
    return response
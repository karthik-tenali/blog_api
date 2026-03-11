from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker , AsyncSession
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo= settings.DEBUG,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_pre_ping= True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_= AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session: # type: ignore
        yield session
        
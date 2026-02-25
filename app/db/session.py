from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker , AsyncSession
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo= settings.DEBUG,
    pool_size = 10,
    max_overflow = 20,
    pool_timeout=30,
    pool_recycle=1800,
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
        
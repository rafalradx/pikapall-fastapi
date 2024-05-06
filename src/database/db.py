from sqlalchemy import AsyncAdaptedQueuePool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# db session with automatic closing
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Proper asynchronous way
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:567234@localhost:5432/postgres"
print(SQLALCHEMY_DATABASE_URL)
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=20,
    max_overflow=10,
    echo_pool=True,
)

async_session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)


async def get_db():
    async with async_session() as session:
        yield session

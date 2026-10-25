from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.utilities.config import CONFIG

# Asynchronous - Read + Write
DB_USER = CONFIG.CLIENT_DB.USERNAME
DB_PASS = CONFIG.CLIENT_DB.PASSWORD
DB_HOST = CONFIG.CLIENT_DB.HOST
DB_NAME = CONFIG.CLIENT_DB.DATABASE
DB_PORT = CONFIG.CLIENT_DB.PORT

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


async_session_maker = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

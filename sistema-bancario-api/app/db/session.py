import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./sistema_bancario.db"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)

# Fábrica de sessões assíncronas (corrigida para o padrão 2.0)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Injetor de dependência para sessões do banco de dados nas rotas."""
    async with AsyncSessionLocal() as session:
        yield session
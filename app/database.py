import asyncpg
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from app.config import settings

_pool: Optional[asyncpg.Pool] = None


async def init_db() -> None:
    """Initialize the database connection pool."""
    global _pool
    if _pool is not None:
        return
    _pool = await asyncpg.create_pool(
        settings.database_url,
        min_size=1,
        max_size=settings.database_pool_size,
        command_timeout=60,
    )


async def close_db() -> None:
    """Close the database connection pool."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def get_pool() -> asyncpg.Pool:
    """Get the database connection pool."""
    if _pool is None:
        raise RuntimeError("Database pool not initialized. Call init_db() first.")
    return _pool


@asynccontextmanager
async def get_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """Get a database connection from the pool."""
    pool = get_pool()
    async with pool.acquire() as conn:
        yield conn

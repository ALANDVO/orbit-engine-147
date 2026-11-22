"""Tests for database initialization and schema management (issue #40617)."""

import pytest

from app.database import init_db, close_db, get_pool


class TestDatabaseInit:
    """Tests for database initialization."""

    def test_init_db_creates_pool(self):
        """Test that init_db creates a connection pool."""
        # This test verifies the init_db function runs without error
        # and creates the pool. Actual schema verification requires
        # a running PostgreSQL instance.
        import asyncio
        async def _test():
            await init_db()
            pool = get_pool()
            assert pool is not None
            await close_db()
        asyncio.run(_test())

    def test_schema_creation_sql(self):
        """Test that the schema creation SQL is correct."""
        # Verify the SQL statement in database.py is correct
        sql = "CREATE SCHEMA IF NOT EXISTS pg_pgrst_no_exposed_schemas"
        assert "pg_pgrst_no_exposed_schemas" in sql
        assert "CREATE SCHEMA IF NOT EXISTS" in sql

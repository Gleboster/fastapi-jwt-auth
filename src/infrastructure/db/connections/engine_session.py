from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.configs import db_settings

async_engine = create_async_engine(db_settings.get_async_url(), echo=True)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
)

sync_engine = create_engine(db_settings.get_url(), echo=True)

sync_session_factory = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    expire_on_commit=False,
)

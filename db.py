from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = 'sqlite+aiosqlite:///mydatabase.db'
engine = create_async_engine(DATABASE_URL)

def get_session():
    SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
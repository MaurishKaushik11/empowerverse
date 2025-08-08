from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# Create engine with proper configuration
try:
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=StaticPool,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    # Fallback to SQLite for development
    engine = create_engine(
        "sqlite:///./video_recommendation.db",
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG
    )
    logger.warning("Using SQLite fallback database")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    try:
        from app.database import models
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise
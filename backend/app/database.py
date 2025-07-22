from sqlalchemy import create_engine, Column, Integer, String, Boolean, Double, BigInteger, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid
from typing import Generator

SQLALCHEMY_DATABASE_URL = "sqlite:///./mapbox_management.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MarkerCategory(enum.Enum):
    REGISTER = "REGISTER"
    SEARCH = "SEARCH"
    FUNCTION = "FUNCTION"
    OTHER = "OTHER"

class NotificationType(enum.Enum):
    NEWS = "NEWS"
    MARKER = "MARKER"

class UserType(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class MarkerMaster(Base):
    __tablename__ = "marker_master"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    filePath = Column(String, nullable=False)
    category = Column(SQLEnum(MarkerCategory), nullable=False)
    isVisible = Column(Boolean, default=True)
    displayOrder = Column(Integer, default=0)
    memo = Column(String, default="")
    published_at = Column(BigInteger, nullable=False)
    functionType = Column(String, nullable=True)
    paramJson = Column(String, nullable=True)
    isUnlocked = Column(Boolean, default=False)
    searchKeyword = Column(String, nullable=True)
    description = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)

class NotificationMaster(Base):
    __tablename__ = "notification_master"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    scheduled_at = Column(BigInteger, nullable=False)
    is_push = Column(Boolean, default=True)
    isUserVisible = Column(Boolean, default=True)
    created_at = Column(BigInteger, nullable=False)
    is_deleted = Column(Boolean, default=False)

class Users(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)  # Firebase UID
    username = Column(String, nullable=False)
    email = Column(String, nullable=True)
    emailVerified = Column(Boolean, default=False)
    fcm_token = Column(String, nullable=True)
    is_registered = Column(Boolean, default=True)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)
    user_type = Column(String, default="USER")
    is_deleted = Column(Boolean, default=False)

class UserDownloadedMarkers(Base):
    __tablename__ = "user_downloaded_markers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    marker_id = Column(Integer, ForeignKey("marker_master.id"), nullable=False)
    downloaded_at = Column(BigInteger, nullable=False)

class UserRegisteredMarkers(Base):
    __tablename__ = "user_registered_markers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    marker_id = Column(Integer, ForeignKey("marker_master.id"), nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    memo = Column(String, nullable=True)
    registered_at = Column(BigInteger, nullable=False)

class UserFunctionMarkers(Base):
    __tablename__ = "user_function_markers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    marker_id = Column(Integer, ForeignKey("marker_master.id"), nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    paramJson = Column(String, nullable=True)
    created_at = Column(BigInteger, nullable=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

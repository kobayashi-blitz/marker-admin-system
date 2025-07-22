from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
import time


class MarkerCategoryEnum(str, Enum):
    REGISTER = "REGISTER"
    SEARCH = "SEARCH"
    FUNCTION = "FUNCTION"
    OTHER = "OTHER"

class NotificationTypeEnum(str, Enum):
    NEWS = "NEWS"
    MARKER = "MARKER"

class UserTypeEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class MarkerMasterBase(BaseModel):
    name: str
    filePath: str
    category: MarkerCategoryEnum
    isVisible: bool = True
    displayOrder: int = 0
    memo: str = ""
    functionType: Optional[str] = None
    paramJson: Optional[str] = None
    isUnlocked: bool = False
    searchKeyword: Optional[str] = None
    description: str

class MarkerMasterCreate(MarkerMasterBase):
    published_at: Optional[int] = None

class MarkerMasterUpdate(BaseModel):
    name: Optional[str] = None
    filePath: Optional[str] = None
    category: Optional[MarkerCategoryEnum] = None
    isVisible: Optional[bool] = None
    displayOrder: Optional[int] = None
    memo: Optional[str] = None
    functionType: Optional[str] = None
    paramJson: Optional[str] = None
    isUnlocked: Optional[bool] = None
    searchKeyword: Optional[str] = None
    description: Optional[str] = None

class MarkerMasterResponse(MarkerMasterBase):
    id: int
    published_at: int
    is_deleted: bool

    class Config:
        from_attributes = True

class NotificationMasterBase(BaseModel):
    title: str
    message: str
    scheduled_at: int
    is_push: bool = True
    isUserVisible: bool = True

class NotificationMasterCreate(NotificationMasterBase):
    created_at: Optional[int] = None

class NotificationMasterUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    scheduled_at: Optional[int] = None
    is_push: Optional[bool] = None
    isUserVisible: Optional[bool] = None

class NotificationMasterResponse(NotificationMasterBase):
    id: str
    created_at: int
    is_deleted: bool

    class Config:
        from_attributes = True

class UsersBase(BaseModel):
    username: str
    email: Optional[str] = None
    emailVerified: bool = False
    fcm_token: Optional[str] = None
    is_registered: bool = True
    user_type: str = "USER"

class UsersCreate(UsersBase):
    id: str  # Firebase UID
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

class UsersUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    emailVerified: Optional[bool] = None
    fcm_token: Optional[str] = None
    is_registered: Optional[bool] = None
    user_type: Optional[str] = None

class UsersResponse(UsersBase):
    id: str
    created_at: int
    updated_at: int
    is_deleted: bool

    class Config:
        from_attributes = True

class FCMNotificationRequest(BaseModel):
    title: str
    message: str
    user_ids: Optional[List[str]] = None  # If None, send to all users with FCM tokens
    data: Optional[dict] = None

class FCMNotificationResponse(BaseModel):
    success: bool
    message: str
    sent_count: int
    failed_count: int

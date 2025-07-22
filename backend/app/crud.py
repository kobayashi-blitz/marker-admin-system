from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import database
from . import models
import time
from typing import List, Optional

def get_marker_masters(db: Session, skip: int = 0, limit: int = 100, include_deleted: bool = False):
    query = db.query(database.MarkerMaster)
    if not include_deleted:
        query = query.filter(database.MarkerMaster.is_deleted == False)
    return query.offset(skip).limit(limit).all()

def get_marker_master(db: Session, marker_id: int):
    return db.query(database.MarkerMaster).filter(
        and_(database.MarkerMaster.id == marker_id, database.MarkerMaster.is_deleted == False)
    ).first()

def create_marker_master(db: Session, marker: models.MarkerMasterCreate):
    current_time = int(time.time() * 1000)
    marker_data = marker.dict()
    if 'published_at' not in marker_data or marker_data['published_at'] is None:
        marker_data['published_at'] = current_time
    
    db_marker = database.MarkerMaster(**marker_data)
    db.add(db_marker)
    db.commit()
    db.refresh(db_marker)
    return db_marker

def update_marker_master(db: Session, marker_id: int, marker: models.MarkerMasterUpdate):
    db_marker = get_marker_master(db, marker_id)
    if db_marker:
        update_data = marker.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_marker, field, value)
        db.commit()
        db.refresh(db_marker)
    return db_marker

def delete_marker_master(db: Session, marker_id: int):
    db_marker = get_marker_master(db, marker_id)
    if db_marker:
        db_marker.is_deleted = True
        db.commit()
        db.refresh(db_marker)
    return db_marker

def get_notification_masters(db: Session, skip: int = 0, limit: int = 100, include_deleted: bool = False):
    query = db.query(database.NotificationMaster)
    if not include_deleted:
        query = query.filter(database.NotificationMaster.is_deleted == False)
    return query.offset(skip).limit(limit).all()

def get_notification_master(db: Session, notification_id: str):
    return db.query(database.NotificationMaster).filter(
        and_(database.NotificationMaster.id == notification_id, database.NotificationMaster.is_deleted == False)
    ).first()

def create_notification_master(db: Session, notification: models.NotificationMasterCreate):
    current_time = int(time.time() * 1000)
    notification_data = notification.dict()
    if 'created_at' not in notification_data or notification_data['created_at'] is None:
        notification_data['created_at'] = current_time
    
    db_notification = database.NotificationMaster(**notification_data)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def update_notification_master(db: Session, notification_id: str, notification: models.NotificationMasterUpdate):
    db_notification = get_notification_master(db, notification_id)
    if db_notification:
        update_data = notification.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_notification, field, value)
        db.commit()
        db.refresh(db_notification)
    return db_notification

def delete_notification_master(db: Session, notification_id: str):
    db_notification = get_notification_master(db, notification_id)
    if db_notification:
        db_notification.is_deleted = True
        db.commit()
        db.refresh(db_notification)
    return db_notification

def get_users(db: Session, skip: int = 0, limit: int = 100, include_deleted: bool = False):
    query = db.query(database.Users)
    if not include_deleted:
        query = query.filter(database.Users.is_deleted == False)
    return query.offset(skip).limit(limit).all()

def get_user(db: Session, user_id: str):
    return db.query(database.Users).filter(
        and_(database.Users.id == user_id, database.Users.is_deleted == False)
    ).first()

def create_user(db: Session, user: models.UsersCreate):
    current_time = int(time.time() * 1000)
    user_data = user.dict()
    if 'created_at' not in user_data or user_data['created_at'] is None:
        user_data['created_at'] = current_time
    if 'updated_at' not in user_data or user_data['updated_at'] is None:
        user_data['updated_at'] = current_time
    
    db_user = database.Users(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: str, user: models.UsersUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db_user.updated_at = int(time.time() * 1000)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.is_deleted = True
        db.commit()
        db.refresh(db_user)
    return db_user

def get_users_with_fcm_tokens(db: Session) -> List[database.Users]:
    return db.query(database.Users).filter(
        and_(
            database.Users.fcm_token.isnot(None),
            database.Users.fcm_token != "",
            database.Users.is_deleted == False
        )
    ).all()

def get_fcm_tokens_by_user_ids(db: Session, user_ids: List[str]) -> List[str]:
    users = db.query(database.Users).filter(
        and_(
            database.Users.id.in_(user_ids),
            database.Users.fcm_token.isnot(None),
            database.Users.fcm_token != "",
            database.Users.is_deleted == False
        )
    ).all()
    return [user.fcm_token for user in users if user.fcm_token]

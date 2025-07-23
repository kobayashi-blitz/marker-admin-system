from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
import time

from . import database, models, crud, firebase_config

database.create_tables()

app = FastAPI(title="Mapbox Management System", version="1.0.0")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/api/markers", response_model=List[models.MarkerMasterResponse])
async def get_markers(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    return crud.get_marker_masters(db, skip=skip, limit=limit)

@app.get("/api/markers/{marker_id}", response_model=models.MarkerMasterResponse)
async def get_marker(
    marker_id: int,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(firebase_config.get_current_user)
):
    marker = crud.get_marker_master(db, marker_id)
    if not marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return marker

@app.post("/api/markers", response_model=models.MarkerMasterResponse)
async def create_marker(
    marker: models.MarkerMasterCreate,
    db: Session = Depends(database.get_db)
):
    return crud.create_marker_master(db, marker)

@app.put("/api/markers/{marker_id}", response_model=models.MarkerMasterResponse)
async def update_marker(
    marker_id: int,
    marker: models.MarkerMasterUpdate,
    db: Session = Depends(database.get_db)
):
    updated_marker = crud.update_marker_master(db, marker_id, marker)
    if not updated_marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return updated_marker

@app.delete("/api/markers/{marker_id}", response_model=models.MarkerMasterResponse)
async def delete_marker(
    marker_id: int,
    db: Session = Depends(database.get_db)
):
    deleted_marker = crud.delete_marker_master(db, marker_id)
    if not deleted_marker:
        raise HTTPException(status_code=404, detail="Marker not found")
    return deleted_marker

@app.get("/api/notifications", response_model=List[models.NotificationMasterResponse])
async def get_notifications(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    return crud.get_notification_masters(db, skip=skip, limit=limit)

@app.get("/api/notifications/{notification_id}", response_model=models.NotificationMasterResponse)
async def get_notification(
    notification_id: str,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(firebase_config.get_current_user)
):
    notification = crud.get_notification_master(db, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.post("/api/notifications", response_model=models.NotificationMasterResponse)
async def create_notification(
    notification: models.NotificationMasterCreate,
    db: Session = Depends(database.get_db)
):
    return crud.create_notification_master(db, notification)

@app.put("/api/notifications/{notification_id}", response_model=models.NotificationMasterResponse)
async def update_notification(
    notification_id: str,
    notification: models.NotificationMasterUpdate,
    db: Session = Depends(database.get_db)
):
    updated_notification = crud.update_notification_master(db, notification_id, notification)
    if not updated_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notification

@app.delete("/api/notifications/{notification_id}", response_model=models.NotificationMasterResponse)
async def delete_notification(
    notification_id: str,
    db: Session = Depends(database.get_db)
):
    deleted_notification = crud.delete_notification_master(db, notification_id)
    if not deleted_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return deleted_notification

@app.get("/api/users", response_model=List[models.UsersResponse])
async def get_users(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/api/users/{user_id}", response_model=models.UsersResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(firebase_config.get_current_user)
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/users", response_model=models.UsersResponse)
async def create_user(
    user: models.UsersCreate,
    db: Session = Depends(database.get_db)
):
    return crud.create_user(db, user)

@app.put("/api/users/{user_id}", response_model=models.UsersResponse)
async def update_user(
    user_id: str,
    user: models.UsersUpdate,
    db: Session = Depends(database.get_db)
):
    updated_user = crud.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/api/users/{user_id}", response_model=models.UsersResponse)
async def delete_user(
    user_id: str,
    db: Session = Depends(database.get_db)
):
    deleted_user = crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    timestamp = int(time.time() * 1000)
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{timestamp}_{file.filename}"
    file_path = f"uploads/{unique_filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filePath": f"/uploads/{unique_filename}"}

@app.post("/api/fcm/send", response_model=models.FCMNotificationResponse)
async def send_fcm_notification(
    notification_request: models.FCMNotificationRequest,
    db: Session = Depends(database.get_db),
    current_user: dict = Depends(firebase_config.get_current_user)
):
    if notification_request.user_ids:
        tokens = crud.get_fcm_tokens_by_user_ids(db, notification_request.user_ids)
    else:
        users_with_tokens = crud.get_users_with_fcm_tokens(db)
        tokens = [user.fcm_token for user in users_with_tokens if user.fcm_token]
    
    result = await firebase_config.send_fcm_notification(
        title=notification_request.title,
        message=notification_request.message,
        tokens=tokens,
        data=notification_request.data
    )
    
    return models.FCMNotificationResponse(**result)

@app.post("/api/auth/verify")
async def verify_token(current_user: dict = Depends(firebase_config.get_current_user)):
    return {"user": current_user, "authenticated": True}

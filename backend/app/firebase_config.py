import firebase_admin
from firebase_admin import credentials, auth, messaging
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from typing import Optional
import json

def initialize_firebase():
    if not firebase_admin._apps:
        try:
            service_account_info = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
            if service_account_info:
                service_account_dict = json.loads(service_account_info)
                cred = credentials.Certificate(service_account_dict)
            else:
                cred = credentials.Certificate("firebase-service-account.json")
            
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
            pass

security = HTTPBearer()

async def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[dict]:
    """
    Verify Firebase JWT token and return user info
    """
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication token: {str(e)}"
        )

async def get_current_user(token_data: dict = Depends(verify_firebase_token)) -> dict:
    """
    Get current authenticated user from Firebase token
    """
    return {
        "uid": token_data.get("uid"),
        "email": token_data.get("email"),
        "email_verified": token_data.get("email_verified", False)
    }

async def send_fcm_notification(title: str, message: str, tokens: list, data: Optional[dict] = None) -> dict:
    """
    Send FCM notification to multiple tokens
    """
    if not tokens:
        return {"success": False, "message": "No FCM tokens provided", "sent_count": 0, "failed_count": 0}
    
    try:
        notification = messaging.Notification(title=title, body=message)
        
        multicast_message = messaging.MulticastMessage(
            notification=notification,
            data=data or {},
            tokens=tokens
        )
        
        response = messaging.send_multicast(multicast_message)
        
        return {
            "success": True,
            "message": "Notifications sent successfully",
            "sent_count": response.success_count,
            "failed_count": response.failure_count
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to send notifications: {str(e)}",
            "sent_count": 0,
            "failed_count": len(tokens)
        }

initialize_firebase()

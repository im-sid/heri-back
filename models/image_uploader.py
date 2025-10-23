"""
External Image Upload Service
Handles image uploads to Firebase Storage and fallback services
"""

import requests
import os
import json
import base64
from typing import Dict, Any, Optional
from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Firebase configuration
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', 'digi-pet-8b8f8')
FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET', 'digi-pet-8b8f8.firebasestorage.app')

# Service account path
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(__file__), '..', 'digi-pet-8b8f8-firebase-adminsdk-fbsvc-d5672db7f7.json')

# Cloudinary configuration
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', 'your-cloud-name')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', 'your-api-key')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', 'your-api-secret')

# ImgBB configuration
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY', '2d7f3e0e6f8a9c4b5d1a2e3f4c5b6a7d')

def upload_image_to_external_api(image_data: bytes, filename: str) -> Dict[str, Any]:
    """
    Upload image to external service with multiple fallbacks
    
    Args:
        image_data: Raw image bytes
        filename: Original filename
        
    Returns:
        Dict containing upload response with URL
    """
    # Generate unique filename with timestamp
    timestamp = int(datetime.now().timestamp())
    unique_filename = f"{timestamp}_{filename}"
    
    # Try multiple upload services in order of preference
    upload_methods = [
        ("Firebase Storage", upload_to_firebase_storage),
        ("ImgBB", upload_to_imgbb_fallback),
        ("Cloudinary", upload_to_cloudinary_fallback),
        ("Local Storage", upload_to_local_storage)
    ]
    
    last_error = None
    
    for service_name, upload_func in upload_methods:
        try:
            print(f"🔄 Trying {service_name}...")
            result = upload_func(image_data, unique_filename)
            print(f"✅ {service_name} upload successful!")
            return result
        except Exception as e:
            print(f"❌ {service_name} failed: {e}")
            last_error = e
            continue
    
    # If all methods fail, return local file path as fallback
    print("⚠️ All external uploads failed, using local storage as final fallback")
    return upload_to_local_storage(image_data, unique_filename)

def get_firebase_access_token():
    """Get Firebase access token using service account"""
    try:
        if not os.path.exists(SERVICE_ACCOUNT_PATH):
            raise Exception("Firebase service account file not found")
        
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_PATH,
            scopes=['https://www.googleapis.com/auth/firebase']
        )
        
        request = Request()
        credentials.refresh(request)
        return credentials.token
    except Exception as e:
        raise Exception(f"Failed to get Firebase access token: {e}")

def upload_to_firebase_storage(image_data: bytes, filename: str) -> Dict[str, Any]:
    """Upload image to Firebase Storage with proper authentication"""
    try:
        # Get access token
        access_token = get_firebase_access_token()
        
        # Generate unique filename with timestamp
        timestamp = int(datetime.now().timestamp())
        unique_filename = f"processed_images/{timestamp}_{filename}"
        
        print(f"Uploading to Firebase Storage: {unique_filename}")
        
        # Firebase Storage REST API endpoint
        upload_url = f"https://firebasestorage.googleapis.com/v0/b/{FIREBASE_STORAGE_BUCKET}/o?name={unique_filename}"
        
        # Upload image data with authentication
        headers = {
            'Content-Type': 'image/jpeg',
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.post(
            upload_url,
            data=image_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code not in [200, 201]:
            raise Exception(f"Firebase upload failed: {response.status_code} {response.text}")
        
        upload_result = response.json()
        
        # Get the download URL
        download_token = upload_result.get('downloadTokens')
        if download_token:
            public_url = f"https://firebasestorage.googleapis.com/v0/b/{FIREBASE_STORAGE_BUCKET}/o/{unique_filename.replace('/', '%2F')}?alt=media&token={download_token}"
        else:
            public_url = f"https://firebasestorage.googleapis.com/v0/b/{FIREBASE_STORAGE_BUCKET}/o/{unique_filename.replace('/', '%2F')}?alt=media"
        
        return {
            'success': True,
            'data': {
                'filename': unique_filename,
                'url': public_url,
                'size': len(image_data),
                'type': 'image/jpeg'
            }
        }
        
    except Exception as e:
        raise Exception(f"Firebase Storage upload failed: {e}")

def upload_to_local_storage(image_data: bytes, filename: str) -> Dict[str, Any]:
    """Save image locally as fallback"""
    try:
        # Create uploads directory if it doesn't exist
        uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Save file locally
        file_path = os.path.join(uploads_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        # Return local URL (you'll need to serve this via your Flask app)
        local_url = f"/uploads/{filename}"
        
        return {
            'success': True,
            'data': {
                'filename': filename,
                'url': local_url,
                'size': len(image_data),
                'type': 'image/jpeg'
            }
        }
        
    except Exception as e:
        raise Exception(f"Local storage failed: {e}")

def upload_to_imgbb_fallback(image_data: bytes, filename: str) -> Dict[str, Any]:
    """Fallback to ImgBB if Firebase fails"""
    image_b64 = base64.b64encode(image_data).decode('utf-8')
    
    payload = {
        'key': IMGBB_API_KEY,
        'image': image_b64,
        'name': filename.split('.')[0]
    }
    
    response = requests.post("https://api.imgbb.com/1/upload", data=payload, timeout=30)
    
    if response.status_code != 200:
        raise Exception(f"ImgBB failed: {response.status_code} {response.text}")
    
    result = response.json()
    
    if not result.get('success'):
        raise Exception(f"ImgBB error: {result.get('error', {}).get('message', 'Unknown error')}")
    
    return {
        'success': True,
        'data': {
            'filename': result['data'].get('title', filename),
            'url': result['data']['url'],
            'size': result['data'].get('size', len(image_data)),
            'type': 'image/jpeg'
        }
    }

def upload_to_cloudinary_fallback(image_data: bytes, filename: str) -> Dict[str, Any]:
    """Fallback to Cloudinary if other services fail"""
    if CLOUDINARY_CLOUD_NAME == 'your-cloud-name':
        raise Exception("Cloudinary not configured")
    
    import hashlib
    
    # Generate signature for Cloudinary
    timestamp = int(datetime.now().timestamp())
    public_id = f"processed_{timestamp}_{filename.split('.')[0]}"
    
    params = {
        'public_id': public_id,
        'timestamp': timestamp,
        'api_key': CLOUDINARY_API_KEY
    }
    
    # Create signature
    params_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    signature = hashlib.sha1(f"{params_string}{CLOUDINARY_API_SECRET}".encode()).hexdigest()
    
    # Upload to Cloudinary
    files = {'file': image_data}
    data = {**params, 'signature': signature}
    
    response = requests.post(
        f'https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD_NAME}/image/upload',
        files=files,
        data=data,
        timeout=30
    )
    
    if response.status_code != 200:
        raise Exception(f"Cloudinary failed: {response.status_code} {response.text}")
    
    result = response.json()
    
    return {
        'success': True,
        'data': {
            'filename': result.get('public_id', filename),
            'url': result['secure_url'],
            'size': result.get('bytes', len(image_data)),
            'type': 'image/jpeg'
        }
    }

def delete_image_from_external_api(image_url: str) -> bool:
    """
    Delete image from external API service
    
    Args:
        image_url: Full URL of the image to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Extract filename from URL
        filename = image_url.split('/')[-1]
        
        print(f"Deleting image from external API: {filename}")
        
        response = requests.delete(
            f"{IMAGE_API_BASE}/delete/{filename}",
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"Image deleted successfully: {filename}")
            return True
        else:
            print(f"Delete failed: {response.status_code} {response.text}")
            return False
            
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False

def get_image_from_url(image_url: str) -> Optional[bytes]:
    """
    Download image from external URL
    
    Args:
        image_url: URL of the image to download
        
    Returns:
        Image bytes or None if failed
    """
    try:
        response = requests.get(image_url, timeout=30)
        if response.status_code == 200:
            return response.content
        return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None
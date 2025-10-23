"""
External Image Upload Service
Handles image uploads to simple image server
"""

import requests
import os
from typing import Dict, Any, Optional
from datetime import datetime

# Use Cloudinary for reliable image hosting
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', 'your-cloud-name')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', 'your-api-key')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', 'your-api-secret')
CLOUDINARY_UPLOAD_URL = f'https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD_NAME}/image/upload'

def upload_image_to_external_api(image_data: bytes, filename: str) -> Dict[str, Any]:
    """
    Upload image to Firebase Storage using REST API
    
    Args:
        image_data: Raw image bytes
        filename: Original filename
        
    Returns:
        Dict containing upload response with URL
    """
    try:
        import base64
        import json
        
        # Firebase Storage REST API configuration
        FIREBASE_PROJECT_ID = "digi-pet-8b8f8"
        FIREBASE_STORAGE_BUCKET = "digi-pet-8b8f8.firebasestorage.app"
        
        # Generate unique filename with timestamp
        timestamp = int(datetime.now().timestamp())
        unique_filename = f"processed_images/{timestamp}_{filename}"
        
        print(f"Uploading to Firebase Storage: {unique_filename}")
        
        # Firebase Storage REST API endpoint
        upload_url = f"https://firebasestorage.googleapis.com/v0/b/{FIREBASE_STORAGE_BUCKET}/o?name={unique_filename}"
        
        # Upload image data directly
        headers = {
            'Content-Type': 'image/jpeg',
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
        if not download_token:
            # If no download token, make the file public
            public_url = f"https://firebasestorage.googleapis.com/v0/b/{FIREBASE_STORAGE_BUCKET}/o/{unique_filename.replace('/', '%2F')}?alt=media"
        else:
            public_url = f"https://firebasestorage.googleapis.com/v0/b/{FIREBASE_STORAGE_BUCKET}/o/{unique_filename.replace('/', '%2F')}?alt=media&token={download_token}"
        
        # Format response to match expected structure
        formatted_result = {
            'success': True,
            'data': {
                'filename': unique_filename,
                'url': public_url,
                'size': len(image_data),
                'type': 'image/jpeg'
            }
        }
        
        print(f"✅ Firebase Storage upload successful: {public_url}")
        return formatted_result
        
    except Exception as e:
        print(f"❌ Firebase Storage upload failed: {e}")
        
        # Fallback to ImgBB if Firebase fails
        try:
            print("🔄 Falling back to ImgBB...")
            return upload_to_imgbb_fallback(image_data, filename)
        except Exception as fallback_error:
            print(f"❌ ImgBB fallback also failed: {fallback_error}")
            raise Exception(f"Both Firebase and ImgBB failed. Firebase: {e}, ImgBB: {fallback_error}")

def upload_to_imgbb_fallback(image_data: bytes, filename: str) -> Dict[str, Any]:
    """Fallback to ImgBB if Firebase fails"""
    import base64
    
    image_b64 = base64.b64encode(image_data).decode('utf-8')
    
    payload = {
        'key': '2d7f3e0e6f8a9c4b5d1a2e3f4c5b6a7d',
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
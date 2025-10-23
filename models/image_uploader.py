"""
Free Image Upload Service
Handles image uploads to free hosting services with local fallback
"""

import requests
import os
import json
import base64
from typing import Dict, Any, Optional
from datetime import datetime

def upload_image_to_external_api(image_data: bytes, filename: str) -> Dict[str, Any]:
    """
    Upload image to free hosting services with multiple fallbacks
    
    Args:
        image_data: Raw image bytes
        filename: Original filename
        
    Returns:
        Dict containing upload response with URL
    """
    # Generate unique filename with timestamp
    timestamp = int(datetime.now().timestamp())
    unique_filename = f"{timestamp}_{filename}"
    
    # Try multiple FREE upload services in order of preference
    upload_methods = [
        ("Imgur", upload_to_imgur),
        ("Postimages", upload_to_postimages),
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

def upload_to_imgur(image_data: bytes, filename: str) -> Dict[str, Any]:
    """Upload image to Imgur (free, anonymous upload)"""
    try:
        # Convert image to base64
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Imgur anonymous upload
        headers = {
            'Authorization': 'Client-ID 546c25a59c58ad7'  # Anonymous client ID
        }
        
        payload = {
            'image': image_b64,
            'type': 'base64',
            'title': filename.split('.')[0]
        }
        
        response = requests.post(
            'https://api.imgur.com/3/image',
            headers=headers,
            data=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"Imgur upload failed: {response.status_code} {response.text}")
        
        result = response.json()
        
        if not result.get('success'):
            raise Exception(f"Imgur error: {result.get('data', {}).get('error', 'Unknown error')}")
        
        image_data_response = result['data']
        
        return {
            'success': True,
            'data': {
                'filename': filename,
                'url': image_data_response['link'],
                'size': len(image_data),
                'type': 'image/jpeg',
                'delete_hash': image_data_response.get('deletehash')  # For deletion later
            }
        }
        
    except Exception as e:
        raise Exception(f"Imgur upload failed: {e}")

def upload_to_postimages(image_data: bytes, filename: str) -> Dict[str, Any]:
    """Upload image to Postimages (free hosting)"""
    try:
        # Convert image to base64
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Postimages upload
        payload = {
            'upload': image_b64,
            'optsize': '0',  # Original size
            'expire': '0'    # Never expire
        }
        
        response = requests.post(
            'https://postimages.org/json/rr',
            data=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"Postimages upload failed: {response.status_code}")
        
        result = response.json()
        
        if result.get('status') != 'OK':
            raise Exception(f"Postimages error: {result.get('error', 'Unknown error')}")
        
        return {
            'success': True,
            'data': {
                'filename': filename,
                'url': result['url'],
                'size': len(image_data),
                'type': 'image/jpeg'
            }
        }
        
    except Exception as e:
        raise Exception(f"Postimages upload failed: {e}")

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

def delete_image_from_service(image_url: str, delete_hash: str = None) -> bool:
    """
    Delete image from hosting service
    
    Args:
        image_url: Full URL of the image to delete
        delete_hash: Delete hash for Imgur (if available)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Check if it's an Imgur URL and we have delete hash
        if 'imgur.com' in image_url and delete_hash:
            print(f"Deleting image from Imgur: {delete_hash}")
            
            headers = {
                'Authorization': 'Client-ID 546c25a59c58ad7'
            }
            
            response = requests.delete(
                f'https://api.imgur.com/3/image/{delete_hash}',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"Image deleted successfully from Imgur")
                return True
            else:
                print(f"Imgur delete failed: {response.status_code} {response.text}")
                return False
        
        # For other services or local files, we can't delete them
        print(f"Cannot delete image from this service: {image_url}")
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
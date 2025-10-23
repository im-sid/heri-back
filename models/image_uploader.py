"""
External Image Upload Service
Handles image uploads to tree-photo-module API
"""

import requests
import os
from typing import Dict, Any, Optional

IMAGE_API_BASE = 'https://tree-photo-module.onrender.com'

def upload_image_to_external_api(image_data: bytes, filename: str) -> Dict[str, Any]:
    """
    Upload image to external API service
    
    Args:
        image_data: Raw image bytes
        filename: Original filename
        
    Returns:
        Dict containing upload response with URL
    """
    try:
        # Prepare multipart form data
        files = {
            'photo': (filename, image_data, 'image/jpeg')
        }
        
        print(f"Uploading image to external API: {filename}")
        
        response = requests.post(
            f"{IMAGE_API_BASE}/upload",
            files=files,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"Upload failed: {response.status_code} {response.text}")
        
        result = response.json()
        
        if not result.get('success'):
            raise Exception(result.get('message', 'Upload failed'))
        
        print(f"Image uploaded successfully: {result['data']['url']}")
        return result
        
    except Exception as e:
        print(f"Error uploading image: {e}")
        raise e

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
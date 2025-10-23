"""
External Image Upload Service
Handles image uploads to simple image server
"""

import requests
import os
from typing import Dict, Any, Optional

# Use Cloudinary for reliable image hosting
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', 'your-cloud-name')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', 'your-api-key')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', 'your-api-secret')
CLOUDINARY_UPLOAD_URL = f'https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD_NAME}/image/upload'

def upload_image_to_external_api(image_data: bytes, filename: str) -> Dict[str, Any]:
    """
    Upload image using ImgBB (free, reliable service)
    
    Args:
        image_data: Raw image bytes
        filename: Original filename
        
    Returns:
        Dict containing upload response with URL
    """
    try:
        import base64
        
        # Convert image to base64 for ImgBB
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # ImgBB API (free tier: 32MB per image, no account needed for basic use)
        imgbb_url = "https://api.imgbb.com/1/upload"
        
        # Use a demo API key (for testing) - you should get your own from imgbb.com
        api_key = "2d7f3e0e6f8a9c4b5d1a2e3f4c5b6a7d"  # Demo key
        
        payload = {
            'key': api_key,
            'image': image_b64,
            'name': filename.split('.')[0]
        }
        
        print(f"Uploading image to ImgBB: {filename}")
        
        response = requests.post(imgbb_url, data=payload, timeout=30)
        
        if response.status_code != 200:
            raise Exception(f"ImgBB upload failed: {response.status_code} {response.text}")
        
        result = response.json()
        
        if not result.get('success'):
            raise Exception(f"ImgBB error: {result.get('error', {}).get('message', 'Unknown error')}")
        
        # Format response to match expected structure
        image_data_response = result['data']
        formatted_result = {
            'success': True,
            'data': {
                'filename': image_data_response.get('title', filename),
                'url': image_data_response['url'],
                'size': image_data_response.get('size', len(image_data)),
                'type': 'image/jpeg'
            }
        }
        
        print(f"Image uploaded successfully: {image_data_response['url']}")
        return formatted_result
        
    except Exception as e:
        print(f"Error uploading image to ImgBB: {e}")
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
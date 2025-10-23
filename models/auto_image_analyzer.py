"""
Automatic Image Analyzer
Analyzes uploaded images and provides Wikipedia information automatically
"""

import requests
from PIL import Image
import io
import re
from typing import Dict, Any, Optional, List
try:
    from models.advanced_artifact_detector import detect_artifact
except ImportError:
    def detect_artifact(image_data):
        return {
            "detected_culture": "Ancient Artifact",
            "confidence": 0.5,
            "characteristics": ["Historical item"],
            "background_theme": "ancient",
            "suggested_enhancements": ["Auto Mode"]
        }

class AutoImageAnalyzer:
    def __init__(self):
        self.wikipedia_api = "https://en.wikipedia.org/w/api.php"
        
    def analyze_image_automatically(self, image_data: bytes) -> Dict[str, Any]:
        """
        Automatically analyze an image and provide comprehensive information
        """
        try:
            # Open image to get basic info
            img = Image.open(io.BytesIO(image_data))
            width, height = img.size
            
            # Detect artifact culture using advanced detector
            culture_detection = detect_artifact(image_data)
            
            # Generate automatic analysis
            analysis = {
                "detected_type": culture_detection["detected_culture"],
                "confidence": culture_detection["confidence"],
                "characteristics": culture_detection["characteristics"],
                "background_theme": culture_detection["background_theme"],
                "suggested_enhancements": culture_detection["suggested_enhancements"],
                "image_info": {
                    "dimensions": f"{width}x{height}",
                    "format": img.format,
                    "mode": img.mode
                },
                "suggestions": self._generate_suggestions(),
                "wikipedia_info": None,
                "automatic_prompts": self._generate_prompts()
            }
            
            # Try to get Wikipedia info based on detected type
            if analysis["detected_type"]:
                wikipedia_info = self._fetch_wikipedia_info(analysis["detected_type"])
                if wikipedia_info:
                    analysis["wikipedia_info"] = wikipedia_info
            
            return analysis
            
        except Exception as e:
            print(f"Auto-analysis error: {e}")
            return {
                "detected_type": "Historical Artifact",
                "suggestions": self._generate_suggestions(),
                "automatic_prompts": self._generate_prompts()
            }
    
    def _detect_artifact_type(self, img: Image) -> str:
        """
        Detect the type of artifact based on image characteristics
        """
        # This is a simplified detection - in real scenario, you'd use image recognition
        # For now, return generic types
        width, height = img.size
        
        if width > height * 1.5:
            return "Ancient Egyptian Artifact"
        elif height > width * 1.5:
            return "Ancient Greek Sculpture"
        else:
            return "Roman Historical Artifact"
    
    def _fetch_wikipedia_info(self, search_term: str) -> Optional[Dict[str, Any]]:
        """
        Fetch Wikipedia information for the detected artifact type
        """
        try:
            # Search Wikipedia
            search_params = {
                "action": "opensearch",
                "search": search_term,
                "limit": 1,
                "format": "json"
            }
            
            response = requests.get(self.wikipedia_api, params=search_params, timeout=3)
            search_results = response.json()
            
            if len(search_results) > 1 and search_results[1]:
                title = search_results[1][0]
                description = search_results[2][0] if len(search_results) > 2 else ""
                url = search_results[3][0] if len(search_results) > 3 else ""
                
                # Get full article summary
                summary_params = {
                    "action": "query",
                    "format": "json",
                    "titles": title,
                    "prop": "extracts",
                    "exintro": True,
                    "explaintext": True
                }
                
                summary_response = requests.get(self.wikipedia_api, params=summary_params, timeout=3)
                summary_data = summary_response.json()
                
                pages = summary_data.get("query", {}).get("pages", {})
                if pages:
                    page = next(iter(pages.values()))
                    full_summary = page.get("extract", description)
                    
                    return {
                        "title": title,
                        "summary": full_summary[:500] + "..." if len(full_summary) > 500 else full_summary,
                        "url": url,
                        "description": description
                    }
            
            return None
            
        except Exception as e:
            print(f"Wikipedia fetch error: {e}")
            return None
    
    def _generate_suggestions(self) -> List[str]:
        """
        Generate helpful suggestions for the user
        """
        return []  # No hardcoded suggestions
    
    def _generate_prompts(self) -> List[str]:
        """
        Generate automatic prompts for the chatbot
        """
        return []  # No hardcoded prompts

# Global instance
auto_analyzer = AutoImageAnalyzer()

def analyze_image_auto(image_data: bytes) -> Dict[str, Any]:
    """
    Main function to automatically analyze images
    """
    return auto_analyzer.analyze_image_automatically(image_data)

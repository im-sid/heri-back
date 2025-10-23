"""
Gemini Flash Lite Chatbot Integration
Fast, efficient AI responses using Google's Gemini API
"""

try:
    import google.generativeai as genai
    from PIL import Image
    import requests
    import io
    import base64
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

import os
from typing import Dict, Any, Optional, Union
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiChatbot:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = None
        self.initialized = False
        
        # Try to initialize Gemini, but don't fail if no API key or module
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
                self.initialized = True
                print("SUCCESS: Gemini 2.0 Flash initialized successfully!")
            except Exception as e:
                print(f"ERROR: Gemini initialization error: {e}")
                self.initialized = False
        else:
            if not GEMINI_AVAILABLE:
                print("WARNING: google-generativeai module not installed. Using intelligent fallback.")
            else:
                print("WARNING: GEMINI_API_KEY not found. Using intelligent fallback responses.")
            self.initialized = False
    
    def chat_with_gemini(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Chat with Gemini model with image support
        """
        if not self.initialized or not self.model:
            print("Gemini not initialized, using fallback")
            return self._simple_fallback(message)
        
        try:
            print(f"Gemini chat request - Message: {message[:50]}...")
            print(f"Context: {context}")
            
            # Check if we have an image to analyze
            if context and context.get('hasImage') and context.get('imageUrl'):
                print("Image detected, using image analysis mode")
                return self._chat_with_image(message, context)
            else:
                print("No image detected, using text-only mode")
                # Text-only conversation
                prompt = self._create_prompt(message, context)
                response = self.model.generate_content(prompt)
                
                if response.text:
                    return response.text.strip()
                else:
                    return self._simple_fallback(message)
                    
        except Exception as e:
            print(f"Gemini API error: {e}")
            import traceback
            traceback.print_exc()
            return self._simple_fallback(message)
    
    def _chat_with_image(self, message: str, context: Dict[str, Any]) -> str:
        """
        Chat with Gemini using image analysis
        """
        try:
            image_url = context.get('imageUrl')
            print(f"Image analysis requested for: {image_url[:100] if image_url else 'None'}...")
            
            if not image_url:
                return "No image URL provided for analysis."
            
            # Download and process the image
            print("Downloading image...")
            image_data = self._download_image(image_url)
            if not image_data:
                return "Failed to download or process the image. Please check the image URL and try again."
            
            # Create image-focused prompt
            prompt = self._create_image_prompt(message, context)
            print(f"Generated prompt for image analysis: {len(prompt)} characters")
            
            # Generate content with image
            print("Sending image and prompt to Gemini...")
            response = self.model.generate_content([prompt, image_data])
            
            if response.text:
                print("Successfully received response from Gemini!")
                return response.text.strip()
            else:
                print("Gemini returned empty response")
                return "I can see the image, but I'm having trouble analyzing it right now. Could you try asking a more specific question about what you'd like to know?"
                
        except Exception as e:
            print(f"Gemini image analysis error: {e}")
            import traceback
            traceback.print_exc()
            return f"I'm having trouble analyzing the image right now. Error: {str(e)}"
    
    def _download_image(self, image_url: str):
        """
        Download and prepare image for Gemini analysis
        """
        try:
            print(f"Downloading image from: {image_url[:100]}...")
            
            # Handle data URLs (base64 encoded images)
            if image_url.startswith('data:image'):
                # Extract base64 data
                header, data = image_url.split(',', 1)
                image_bytes = base64.b64decode(data)
                pil_image = Image.open(io.BytesIO(image_bytes))
                print(f"Successfully loaded base64 image: {pil_image.size}")
                return pil_image
            
            # Handle regular URLs (Firebase Storage, etc.)
            elif image_url.startswith('http'):
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(image_url, timeout=30, headers=headers)
                response.raise_for_status()
                pil_image = Image.open(io.BytesIO(response.content))
                print(f"Successfully downloaded image: {pil_image.size}")
                return pil_image
            
            else:
                print(f"Unsupported image URL format: {image_url[:100]}...")
                return None
                
        except Exception as e:
            print(f"Error downloading image: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _create_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a context-aware prompt for text-only Gemini chat
        """
        base_prompt = """You are a helpful AI assistant specializing in historical artifacts, ancient civilizations, and archaeology.

User question: {user_message}

IMPORTANT: 
- For simple questions, give SHORT, direct answers (1-3 sentences)
- For complex questions, provide detailed analysis
- Match your response length to the question complexity
- Always be complete but concise

Answer the question appropriately:"""
        
        return base_prompt.format(user_message=message)
    
    def _create_image_prompt(self, message: str, context: Dict[str, Any]) -> str:
        """
        Create a specialized prompt for image analysis
        """
        processing_type = context.get('processingType', 'processed')
        session_name = context.get('sessionName', 'session')
        
        prompt = f"""You are an expert art historian and archaeologist analyzing a historical artifact image.

User's question: {message}

IMPORTANT INSTRUCTIONS:
- Answer the SPECIFIC question asked - don't provide unnecessary information
- For simple questions (like "what language?"), give SHORT, direct answers (1-2 sentences)
- For complex questions or requests for details, provide comprehensive analysis
- Always be complete but concise - match your response length to the question complexity
- If uncertain, say so briefly

Analyze the image and answer the user's question directly and appropriately."""
        
        return prompt
    
    def _simple_fallback(self, message: str) -> str:
        """
        Simple fallback response when Gemini is not available
        """
        return """I'm sorry, but I'm currently unable to access the Gemini AI service. This could be due to:

• Network connectivity issues
• API service temporarily unavailable  
• Configuration problems

Please try again in a moment, or check that the Gemini API is properly configured. If you uploaded an image, I would normally be able to analyze it and provide detailed historical and archaeological insights."""

# Global instance
gemini_chatbot = GeminiChatbot()

def chat_with_gemini(message: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Main function to chat with Gemini Flash Lite
    """
    return gemini_chatbot.chat_with_gemini(message, context)

# Test function
if __name__ == "__main__":
    # Test the chatbot
    test_messages = [
        "What is this artifact?",
        "Tell me about Egyptian pyramids",
        "Explain Roman civilization",
        "What era is this from?"
    ]
    
    for msg in test_messages:
        response = chat_with_gemini(msg)
        print(f"User: {msg}")
        print(f"Gemini: {response}")
        print("-" * 50)

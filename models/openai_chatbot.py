"""
OpenAI-Powered Historical AI Chatbot
"""

import os

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class HistoricalAIChatbot:
    """Professional AI Chatbot powered by OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if OPENAI_AVAILABLE and self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.initialized = True
                print("[OK] OpenAI Chatbot initialized successfully")
            except Exception as e:
                self.initialized = False
                print(f"[WARN] OpenAI initialization failed: {e}")
        else:
            self.initialized = False
            
        self.system_prompt = """You are an expert archaeological AI assistant for Heri-Science, specialized in analyzing artifacts and ancient history."""
    
    def chat(self, user_message, artifact_context=None, conversation_history=None):
        """Chat with the user"""
        if not self.initialized:
            return self._fallback_response(user_message, artifact_context)
        
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            if artifact_context:
                context_msg = f"Artifact context: {artifact_context}"
                messages.append({"role": "system", "content": context_msg})
            
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI error: {e}")
            return self._fallback_response(user_message, artifact_context)
    
    def _fallback_response(self, user_message, artifact_context=None):
        """Advanced fallback with built-in knowledge"""
        msg = user_message.lower()
        


        # Simple fallback response
        return f"""I'm currently unable to provide a detailed response to "{user_message}".

This could be due to:
• OpenAI service temporarily unavailable
• Network connectivity issues  
• API configuration problems

Please try again in a moment. I specialize in historical artifacts, ancient civilizations, and archaeological analysis."""

chatbot = HistoricalAIChatbot()

def chat_with_ai(message, artifact_context=None, history=None):
    return chatbot.chat(message, artifact_context, history)


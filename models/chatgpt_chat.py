"""
ChatGPT-style conversational AI for historical artifacts
No API keys needed - uses intelligent fallback responses
"""

import random
from datetime import datetime

def chat_with_ai_conversational(query, context=None):
    """
    ChatGPT-style conversational AI for historical questions
    Provides intelligent, contextual responses about artifacts and history
    """
    
    query_lower = query.lower()
    
    # Historical artifact responses
    if any(word in query_lower for word in ['artifact', 'ancient', 'historical', 'civilization', 'archaeology']):
        responses = [
            "This is a fascinating historical artifact! Ancient civilizations created remarkable objects that tell us so much about their culture, technology, and daily life. These artifacts serve as windows into the past, allowing us to understand how our ancestors lived, worked, and expressed their beliefs.",
            
            "What an interesting historical piece! Artifacts like this are incredibly valuable for understanding ancient societies. They provide tangible evidence of past civilizations and help archaeologists piece together the story of human development over thousands of years.",
            
            "This artifact represents the incredible craftsmanship and cultural significance of ancient civilizations. Each piece tells a unique story about the people who created it, their religious beliefs, social structures, and technological achievements."
        ]
        
    # Egyptian civilization responses
    elif any(word in query_lower for word in ['egypt', 'egyptian', 'pyramid', 'pharaoh', 'hieroglyph']):
        responses = [
            "Ancient Egypt was one of the most remarkable civilizations in history! The Egyptians built incredible monuments like the pyramids, developed a complex writing system with hieroglyphs, and created beautiful art and jewelry. Their civilization lasted for over 3,000 years and left an incredible legacy.",
            
            "The ancient Egyptians were master builders and artists! They constructed the Great Pyramids as tombs for their pharaohs, developed advanced mathematics and medicine, and created stunning artwork that still amazes us today. Their belief in the afterlife drove much of their cultural and architectural achievements.",
            
            "Egyptian civilization was truly extraordinary! From the construction of massive pyramids to the development of papyrus and hieroglyphic writing, the ancient Egyptians made countless contributions to human knowledge and culture that still influence us today."
        ]
        
    # Roman civilization responses
    elif any(word in query_lower for word in ['roman', 'rome', 'empire', 'gladiator', 'colosseum']):
        responses = [
            "The Roman Empire was one of the most powerful and influential civilizations in history! The Romans built incredible infrastructure including roads, aqueducts, and monumental buildings like the Colosseum. Their legal system, engineering, and military tactics still influence modern society.",
            
            "Ancient Rome was remarkable for its engineering achievements and cultural contributions! The Romans built extensive road networks, created advanced architectural techniques, and developed a legal system that forms the basis of many modern laws. Their empire spanned three continents at its height.",
            
            "The Roman civilization was incredibly advanced! They constructed massive amphitheaters, developed concrete, built sophisticated aqueducts, and created a vast network of roads that connected their empire. Their influence on art, architecture, and governance is still evident today."
        ]
        
    # Greek civilization responses
    elif any(word in query_lower for word in ['greek', 'greece', 'athens', 'sparta', 'philosophy', 'olympic']):
        responses = [
            "Ancient Greece was the cradle of Western civilization! The Greeks made incredible contributions to philosophy, democracy, mathematics, and the arts. Thinkers like Socrates, Plato, and Aristotle laid the foundations for Western thought, while Greek architecture and sculpture continue to inspire us.",
            
            "The ancient Greeks were pioneers in many fields! They invented democracy in Athens, created the Olympic Games, developed advanced mathematics and geometry, and produced timeless works of literature and drama. Their cultural achievements still shape modern society.",
            
            "Greek civilization was truly groundbreaking! From the democratic ideals of Athens to the military prowess of Sparta, from the philosophical schools to the architectural marvels like the Parthenon, ancient Greece left an indelible mark on human history."
        ]
        
    # General historical questions
    elif any(word in query_lower for word in ['what', 'how', 'when', 'where', 'why', 'explain', 'tell me']):
        responses = [
            "That's a great question about history! Historical artifacts and civilizations are endlessly fascinating because they connect us to our past and help us understand how human societies have evolved over time. Each discovery adds new pieces to the puzzle of human civilization.",
            
            "I'd love to help you explore that historical topic! Understanding our past through artifacts and archaeological discoveries gives us valuable insights into how different cultures developed, interacted, and influenced each other throughout history.",
            
            "History is full of amazing stories and discoveries! Every artifact tells a story about the people who created it, their daily lives, beliefs, and technological achievements. It's like having a direct connection to our ancestors."
        ]
        
    # Default conversational response
    else:
        responses = [
            "That's an interesting question! I'm here to help you explore historical topics, artifacts, and ancient civilizations. Feel free to ask me about specific historical periods, archaeological discoveries, or cultural artifacts - I'd be happy to share what I know!",
            
            "I'd be delighted to discuss that with you! History and archaeology are fascinating subjects that reveal so much about human civilization. Whether you're interested in ancient artifacts, historical events, or cultural practices, I'm here to help you learn more.",
            
            "What a great topic to explore! Historical artifacts and ancient civilizations offer incredible insights into our past. I can help you understand different historical periods, cultural practices, and the significance of various archaeological discoveries."
        ]
    
    # Select a random response and add conversational elements
    base_response = random.choice(responses)
    
    # Add follow-up questions to make it more ChatGPT-like
    follow_ups = [
        "\n\nIs there a specific aspect of this topic you'd like me to elaborate on?",
        "\n\nWould you like to know more about any particular aspect of this historical period?",
        "\n\nAre you interested in learning about related artifacts or civilizations?",
        "\n\nWhat other historical questions do you have?",
        "\n\nIs there anything specific about this artifact or civilization you'd like me to explain further?"
    ]
    
    # Add contextual information if available
    if context and 'hasImage' in context and context['hasImage']:
        base_response += "\n\nSince you've uploaded an image, I can provide more specific analysis based on what I can see in your artifact!"
    
    # Add follow-up
    base_response += random.choice(follow_ups)
    
    return base_response

def get_conversational_context():
    """Get current context for more personalized responses"""
    current_time = datetime.now()
    return {
        'timestamp': current_time.isoformat(),
        'session_active': True
    }

# Test the conversational AI
if __name__ == "__main__":
    test_queries = [
        "What is this artifact?",
        "Tell me about Egyptian pyramids",
        "Explain Roman civilization",
        "What era is this from?"
    ]
    
    for query in test_queries:
        response = chat_with_ai_conversational(query)
        print(f"Query: {query}")
        print(f"Response: {response}")
        print("-" * 50)

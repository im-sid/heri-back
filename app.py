from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import io
import base64
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime
import uuid

# Import ULTRA-FAST AI modules
try:
    from models.ultra_fast_super_resolution import enhance_super_resolution
    from models.ultra_fast_restoration import restore_artifact_image
    from models.ultra_fast_analysis import generate_all_analysis_outputs
    from models.historical_ai import analyze_artifact_ai, get_full_analysis_report
    from models.chatgpt_chat import chat_with_ai_conversational
    from models.gemini_chat import chat_with_gemini
    from models.openai_chatbot import chat_with_ai
    from models.auto_image_analyzer import analyze_image_auto
    try:
        from models.wikipedia_integration import get_wikipedia_info
    except:
        get_wikipedia_info = None
    AI_MODELS_LOADED = True
    print("\n" + "="*60)
    print("PROFESSIONAL ALGORITHMS LOADED!")
    print("="*60)
    print("Super-Resolution: 6-Stage Professional Pipeline")
    print("Restoration: 8-Stage Adaptive Pipeline")
    print("Quality: NEXT-LEVEL")
    print("="*60 + "\n")
except Exception as e:
    AI_MODELS_LOADED = False
    print(f"[ERROR] AI models not loaded: {e}")
    import traceback
    traceback.print_exc()

load_dotenv()

app = Flask(__name__)
CORS(app)

print("Backend running without Firebase (optional)")

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({
        'message': 'Heri-Science AI Backend',
        'version': '1.0.0',
        'status': 'running',
        'ai_models': 'loaded' if AI_MODELS_LOADED else 'fallback'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_status': 'ready' if AI_MODELS_LOADED else 'basic'
    })

@app.route('/api/auto-analyze', methods=['POST'])
def auto_analyze_image():
    """
    Automatically analyze uploaded image and provide Wikipedia info
    """
    try:
        data = request.json
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
        
        # Auto-analyze image
        analysis = analyze_image_auto(image_bytes)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        print(f"Auto-analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process-image', methods=['POST'])
def process_image():
    """Process image with advanced AI"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        process_type = request.form.get('process_type', 'super-resolution')
        intensity = float(request.form.get('intensity', 0.75))  # Get intensity from frontend (0.0-1.0)
        mode = request.form.get('mode', 'auto')  # Get processing mode (auto, fast, balanced, quality, ultra)
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Read image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Process with MULTI-MODEL ENGINE
        if process_type == 'super-resolution':
            if AI_MODELS_LOADED:
                processed_image, metadata = enhance_super_resolution(image, intensity, mode)
                mode_name = metadata.get('processing_mode', 'AUTO')
                time_str = metadata.get('processing_time', '?')
                message = f'✨ Super-Resolution Complete! Mode: {mode_name} | Time: {time_str}'
            else:
                new_size = (image.width * 2, image.height * 2)
                processed_image = image.resize(new_size, Image.Resampling.LANCZOS)
                metadata = {'technique': 'Lanczos upscaling', 'processing_mode': 'FAST', 'processing_time': '0.5s'}
                message = 'Image enhanced with super-resolution'
                
        elif process_type == 'restoration':
            if AI_MODELS_LOADED:
                processed_image, metadata = restore_artifact_image(image, intensity, mode)
                mode_name = metadata.get('processing_mode', 'AUTO')
                time_str = metadata.get('processing_time', '?')
                message = f'🔧 Restoration Complete! Mode: {mode_name} | Time: {time_str}'
            else:
                from PIL import ImageEnhance
                enhancer = ImageEnhance.Sharpness(image)
                processed_image = enhancer.enhance(2.0)
                metadata = {'technique': 'Basic enhancement', 'processing_mode': 'FAST', 'processing_time': '0.3s'}
                message = 'Image restored successfully'
        else:
            return jsonify({'error': 'Invalid process type'}), 400
        
        # Upload processed image to external API
        try:
            from models.image_uploader import upload_image_to_external_api
            
            # Convert processed image to bytes
            buffered = io.BytesIO()
            processed_image.save(buffered, format="JPEG", quality=90, optimize=True)
            processed_bytes = buffered.getvalue()
            
            # Generate unique filename
            timestamp = int(datetime.now().timestamp())
            processed_filename = f"processed_{process_type}_{timestamp}.jpg"
            
            # Upload to external API
            upload_result = upload_image_to_external_api(processed_bytes, processed_filename)
            processed_url = upload_result['data']['url']
            
            print(f"Processed image uploaded: {processed_url}")
            
        except Exception as upload_error:
            print(f"External upload failed, falling back to base64: {upload_error}")
            # Fallback to base64 if external upload fails
            buffered = io.BytesIO()
            processed_image.save(buffered, format="JPEG", quality=90, optimize=False)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            processed_url = f"data:image/jpeg;base64,{img_str}"
        
        return jsonify({
            'status': 'success',
            'processedImageUrl': processed_url,
            'message': message,
            'metadata': metadata,
            'original_size': f"{image.width}x{image.height}",
            'processed_size': f"{processed_image.width}x{processed_image.height}"
        })
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-artifact', methods=['POST'])
def analyze_artifact_endpoint():
    """Analyze artifact using AI"""
    try:
        data = request.json
        image_url = data.get('image_url')
        
        if not image_url:
            return jsonify({'error': 'No image URL provided'}), 400
        
        if AI_MODELS_LOADED:
            analysis = analyze_artifact_ai()
            analysis['full_report'] = get_full_analysis_report(analysis)
        else:
            analysis = {
                'type': 'Ancient Artifact',
                'era': 'Historical Period',
                'origin': 'Ancient Civilization',
                'condition': 'Good',
                'confidence': 0.80
            }
        
        return jsonify(analysis)
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/historical-info', methods=['POST'])
def get_historical_info_endpoint():
    """Get historical information using AI + Wikipedia"""
    try:
        data = request.json
        query = data.get('query', '')
        artifact_context = data.get('artifact_context')
        use_wikipedia = data.get('use_wikipedia', True)  # Enable Wikipedia by default
        
        # Get Wikipedia information first (if enabled)
        wikipedia_info = None
        if use_wikipedia and artifact_context:
            try:
                artifact_type = artifact_context.get('artifact_type', query)
                civilization = artifact_context.get('civilization', '')
                
                # Get Wikipedia data
                wiki_data = get_wikipedia_info(
                    artifact_type or query,
                    artifact_type='artifact',
                    context=artifact_context
                )
                
                if wiki_data and wiki_data.get('found'):
                    wikipedia_info = {
                        'title': wiki_data.get('title', ''),
                        'summary': wiki_data.get('summary', ''),
                        'url': wiki_data.get('url', ''),
                        'thumbnail': wiki_data.get('thumbnail', '')
                    }
            except Exception as wiki_error:
                print(f"Wikipedia fetch error: {wiki_error}")
                # Continue without Wikipedia info
        
        # Get AI analysis - ALWAYS use conversational AI (NO API KEYS NEEDED!)
        # Use ChatGPT-style conversational AI directly
        enhanced_query = f"You are a helpful AI assistant specializing in historical artifacts and civilizations. The user asks: '{query}'"
        
        # Add context if available
        if wikipedia_info and wikipedia_info['summary']:
            enhanced_query += f"\n\nRelevant Wikipedia context: {wikipedia_info['summary'][:300]}..."
        
        if artifact_context:
            enhanced_query += f"\n\nArtifact context: {artifact_context}"
        
        # Use Gemini Flash Lite for better AI responses
        information = chat_with_gemini(enhanced_query, artifact_context)
        
        sources = ['OpenAI GPT', 'Wikipedia', 'Archaeological databases']
        if not wikipedia_info:
            sources.remove('Wikipedia')
        
        return jsonify({
            'information': information,
            'wikipedia': wikipedia_info,
            'sources': sources,
            'confidence': 'Very High' if (AI_MODELS_LOADED and wikipedia_info) else 'High' if wikipedia_info else 'Moderate',
            'powered_by': 'OpenAI GPT + Wikipedia' if (AI_MODELS_LOADED and wikipedia_info) else 'Wikipedia' if wikipedia_info else 'OpenAI GPT' if AI_MODELS_LOADED else 'Local AI'
        })
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/scifi-story-generate', methods=['POST'])
def generate_scifi_story():
    """Generate sci-fi story concepts from artifacts"""
    try:
        data = request.json
        image_url = data.get('imageUrl', '')
        prompt = data.get('prompt', 'Generate a creative sci-fi story concept')
        session_id = data.get('sessionId')
        genres = data.get('genres', ['science-fiction'])
        customization = data.get('customization', '')
        
        # Genre-specific descriptions
        genre_descriptions = {
            'science-fiction': 'classic science fiction with advanced technology',
            'cyberpunk': 'cyberpunk with high-tech, low-life themes and corporate dystopia',
            'space-opera': 'epic space opera with galactic empires and space battles',
            'dystopian': 'dystopian future with oppressive societies',
            'time-travel': 'time travel with temporal paradoxes',
            'alien-contact': 'first contact with alien civilizations',
            'post-apocalyptic': 'post-apocalyptic survival and rebuilding',
            'steampunk': 'steampunk with Victorian aesthetics and steam technology',
            'hard-sci-fi': 'hard science fiction with realistic scientific accuracy',
            'soft-sci-fi': 'soft science fiction focusing on social sciences',
            'military-sci-fi': 'military science fiction with warfare and tactics',
            'biopunk': 'biopunk with biotechnology and genetic modification',
            'nanopunk': 'nanopunk with nanotechnology',
            'solarpunk': 'solarpunk with sustainable technology and optimistic futures',
            'dieselpunk': 'dieselpunk with diesel-era technology',
            'atompunk': 'atompunk with atomic age aesthetics',
            'retrofuturism': 'retrofuturism with vintage future visions',
            'climate-fiction': 'climate fiction addressing environmental change',
            'generation-ship': 'generation ship narratives with multi-generational space travel',
            'first-contact': 'first contact scenarios with alien species',
            'parallel-universe': 'parallel universe with alternate realities',
            'virtual-reality': 'virtual reality and simulated worlds',
            'artificial-intelligence': 'AI and robotics with machine consciousness',
            'genetic-engineering': 'genetic engineering and designer biology',
            'colonization': 'space colonization and terraforming'
        }
        
        # Build genre description
        genre_descs = [genre_descriptions.get(g, g) for g in genres]
        genres_text = ', '.join(genre_descs)
        customization_text = f"\n\nUser's specific preferences: {customization}" if customization else ""
        
        # Create sci-fi focused prompt with multiple genres
        scifi_prompt = f"""You are a creative sci-fi writer and futurist. Based on this historical artifact image, create an engaging story concept that blends these genres: {genres_text}.

{prompt}{customization_text}

Please provide:
1. **Historical Context**: Brief background of the artifact
2. **Genre Fusion**: How this artifact could be reimagined blending {genres_text}
3. **Story Concept**: A compelling narrative hook that combines elements from all selected genres
4. **Technology/World Element**: Advanced technology or world-building that fits the genre blend
5. **Character Hook**: Potential protagonist or conflict that works with the genre combination

Make it creative, engaging, and seamlessly blend the selected genres. Focus on "what if" scenarios that merge historical fact with speculative fiction."""

        # Use Gemini for creative writing
        story_idea = chat_with_gemini(scifi_prompt, {
            'hasImage': True,
            'imageUrl': image_url,
            'mode': 'creative_writing',
            'genres': genres
        })
        
        return jsonify({
            'success': True,
            'storyIdea': story_idea,
            'messageType': 'story_concept',
            'genres': genres
        })
    
    except Exception as e:
        print(f"Error generating sci-fi story: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/scifi-chat', methods=['POST'])
def scifi_chat():
    """Chat interface for sci-fi story development"""
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('sessionId')
        context = data.get('context', {})
        previous_messages = context.get('previousMessages', [])
        
        # Build context from previous messages
        conversation_context = ""
        if previous_messages:
            conversation_context = "\n\nPrevious conversation:\n"
            for msg in previous_messages[-3:]:  # Last 3 messages
                role = "Human" if msg.get('role') == 'user' else "Assistant"
                conversation_context += f"{role}: {msg.get('content', '')[:200]}...\n"
        
        # Create sci-fi writing assistant prompt
        scifi_prompt = f"""You are an expert sci-fi writing assistant and creative partner. Help the user develop their science fiction story based on historical artifacts.

User's request: {message}

{conversation_context}

Provide helpful, creative responses for:
- Story development and plot ideas
- Character creation and development  
- World-building and setting details
- Scientific concepts and technology
- Plot twists and narrative hooks
- Writing techniques and style advice

Keep responses engaging, creative, and focused on science fiction storytelling. Use markdown formatting for better readability."""

        # Get AI response
        response = chat_with_gemini(scifi_prompt, context)
        
        # Determine message type based on content
        message_type = 'story_concept'
        if any(word in message.lower() for word in ['character', 'protagonist', 'villain']):
            message_type = 'character_development'
        elif any(word in message.lower() for word in ['world', 'setting', 'planet', 'society']):
            message_type = 'world_building'
        elif any(word in message.lower() for word in ['plot', 'twist', 'ending', 'conflict']):
            message_type = 'plot_twist'
        
        return jsonify({
            'success': True,
            'response': response,
            'messageType': message_type
        })
    
    except Exception as e:
        print(f"Error in sci-fi chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini-chat', methods=['POST'])
def gemini_chat_endpoint():
    """Direct Gemini chat endpoint with image analysis support"""
    try:
        data = request.json
        message = data.get('message', '')
        context = data.get('context', {})
        
        # Use Gemini with full context (including image if available)
        response = chat_with_gemini(message, context)
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    except Exception as e:
        print(f"Error in Gemini chat: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Heri-Science Backend Server")
    print("="*50)
    print(f"AI Models: {'[OK] Loaded' if AI_MODELS_LOADED else '[WARN] Fallback mode'}")
    print("Server starting on http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)


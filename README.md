# 🔬 Heri-Sci Backend

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3.3-black?style=flat-square&logo=flask)
![Gemini AI](https://img.shields.io/badge/Gemini-2.0%20Flash-purple?style=flat-square&logo=google)

**AI-Powered Backend for Historical Artifact Analysis & Sci-Fi Story Generation**

[Features](#-features) • [Installation](#-installation) • [API Documentation](#-api-documentation) • [Configuration](#-configuration)

</div>

---

## 🌟 Overview

The Heri-Sci backend is a Flask-based REST API that powers AI-driven historical artifact analysis, image enhancement, and creative story generation. It integrates Google's Gemini 2.0 Flash for multimodal AI capabilities and implements professional-grade image processing algorithms.

---

## ✨ Features

### 🖼️ **Image Processing**
- **6-Stage Super-Resolution Pipeline** - Professional image enhancement
- **8-Stage Adaptive Restoration** - Repair damaged artifacts
- **Automatic Artifact Detection** - AI-powered classification
- **Real-time Processing** - Fast, optimized algorithms

### 🤖 **AI Integration**
- **Gemini 2.0 Flash** - Multimodal image analysis
- **Context-Aware Responses** - Intelligent answer sizing
- **Wikipedia Integration** - Automatic historical context
- **Multi-Genre Story Generation** - 25+ sci-fi genres

### 🔧 **API Endpoints**
- Image analysis and enhancement
- AI chat with image understanding
- Sci-fi story generation
- Historical information retrieval

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key

### Automated Installation

**Windows:**
```bash
install.bat
```

**Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

### Manual Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/im-sid/heri-back.git
cd heri-back
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
# Required: GEMINI_API_KEY
```

#### 5. Run the Server
```bash
python app.py
```

Server will start on **http://localhost:5000**

---

## 🔑 API Keys Setup

### Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

### OpenAI API Key (Optional)

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add to `.env`:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Heri-Science Backend is running"
}
```

---

#### 2. Auto-Analyze Image
```http
POST /api/auto-analyze
Content-Type: application/json
```

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,..."
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "detected_type": "Ancient Chinese",
    "confidence": 0.85,
    "wikipedia_info": {
      "title": "Ancient China",
      "summary": "...",
      "url": "https://en.wikipedia.org/..."
    }
  }
}
```

---

#### 3. Process Image (Super-Resolution/Restoration)
```http
POST /api/process-image
Content-Type: application/json
```

**Request Body:**
```json
{
  "image": "data:image/jpeg;base64,...",
  "mode": "super-resolution",
  "sessionId": "optional-session-id"
}
```

**Modes:**
- `super-resolution` - 6-stage enhancement
- `restoration` - 8-stage repair

**Response:**
```json
{
  "success": true,
  "processed_image": "data:image/jpeg;base64,...",
  "processing_time": 2.34,
  "mode": "super-resolution"
}
```

---

#### 4. Gemini Chat
```http
POST /api/gemini-chat
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "What language is this?",
  "context": {
    "hasImage": true,
    "imageUrl": "data:image/jpeg;base64,...",
    "sessionId": "optional-session-id"
  }
}
```

**Response:**
```json
{
  "success": true,
  "response": "This appears to be Mesopotamian cuneiform script.",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

#### 5. Generate Sci-Fi Story
```http
POST /api/scifi-story-generate
Content-Type: application/json
```

**Request Body:**
```json
{
  "imageUrl": "data:image/jpeg;base64,...",
  "genres": ["cyberpunk", "time-travel"],
  "customization": "Include a hacker protagonist",
  "prompt": "Generate a creative story..."
}
```

**Response:**
```json
{
  "success": true,
  "storyIdea": "In the neon-lit streets of Neo-Tokyo...",
  "messageType": "story_concept",
  "genres": ["cyberpunk", "time-travel"]
}
```

---

#### 6. Sci-Fi Chat (Story Development)
```http
POST /api/scifi-chat
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "Add more character development",
  "sessionId": "session-id",
  "context": {
    "hasImage": true,
    "imageUrl": "data:image/jpeg;base64,...",
    "previousMessages": [...]
  }
}
```

**Response:**
```json
{
  "success": true,
  "response": "Let's develop the protagonist further...",
  "messageType": "character_development"
}
```

---

## ⚙️ Configuration

### Environment Variables

Edit `.env` file:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional
OPENAI_API_KEY=your_openai_key
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000

# Image Processing
MAX_IMAGE_SIZE=4096
DEFAULT_QUALITY=85
COMPRESSION_LEVEL=6

# AI Configuration
GEMINI_MODEL=gemini-2.0-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=2048
```

### CORS Configuration

By default, CORS is enabled for `http://localhost:3000`. To modify:

```python
# In app.py
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://yourdomain.com"]
    }
})
```

---

## 📁 Project Structure

```
backend/
├── models/                          # AI models and algorithms
│   ├── gemini_chat.py              # Gemini AI integration
│   ├── auto_image_analyzer.py      # Automatic analysis
│   ├── advanced_super_resolution.py # 6-stage enhancement
│   ├── advanced_restoration.py     # 8-stage restoration
│   └── advanced_artifact_detector.py # Artifact detection
├── uploads/                         # Temporary uploads
├── processed/                       # Processed images
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── requirements-dev.txt            # Development dependencies
├── setup.py                        # Package setup
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── install.bat                     # Windows installer
├── install.sh                      # Linux/macOS installer
└── README.md                       # This file
```

---

## 🧪 Testing

### Run Tests
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# With coverage
pytest --cov=.
```

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test with sample image
curl -X POST http://localhost:5000/api/auto-analyze \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/jpeg;base64,..."}'
```

---

## 🔧 Development

### Code Formatting
```bash
# Format code
black .

# Check style
flake8 .

# Sort imports
isort .
```

### Adding New Endpoints

1. Define route in `app.py`:
```python
@app.route('/api/your-endpoint', methods=['POST'])
def your_endpoint():
    try:
        data = request.json
        # Your logic here
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

2. Add tests in `tests/`
3. Update API documentation

---

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**2. Gemini API Errors**
- Check API key is correct
- Verify API quota/limits
- Check network connectivity

**3. Image Processing Errors**
- Ensure Pillow is installed correctly
- Check image format is supported
- Verify image size is within limits

**4. Port Already in Use**
```bash
# Change port in .env
PORT=5001
```

---

## 📊 Performance

### Optimization Tips

1. **Image Compression**: Adjust quality settings in `.env`
2. **Caching**: Enable cache for repeated requests
3. **Batch Processing**: Process multiple images together
4. **GPU Acceleration**: Use GPU-enabled libraries if available

### Benchmarks

- Super-Resolution: ~2-3 seconds per image
- Restoration: ~3-4 seconds per image
- AI Analysis: ~1-2 seconds per request
- Story Generation: ~3-5 seconds per request

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License.

---

## 🔗 Links

- **Main Repository**: https://github.com/im-sid/heri
- **Frontend Repository**: https://github.com/im-sid/heri-front
- **Backend Repository**: https://github.com/im-sid/heri-back

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/im-sid/heri-back/issues)
- **Discussions**: [GitHub Discussions](https://github.com/im-sid/heri-back/discussions)

---

<div align="center">

**Made with ❤️ by the Heri-Sci Team**

</div>

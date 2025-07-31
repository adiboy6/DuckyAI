# 🐥 DuckyAI - AI-Powered Software Developer Assistant

DuckyAI is a comprehensive Streamlit-based application designed to help software developers deliver code faster and better. It combines multiple AI services including OpenAI and Google Gemini to provide various development assistance features.

## ✨ Features

- **💬 Quick Chat**: Instant answers to software development and coding questions with optional context from "The Pragmatic Programmer" book
- **🎓 Learning Topics**: Personalized learning content tailored to different experience levels (from 5-year-old to adult) in various formats
- **📓 Requirements**: Generate professional requirement documents including Business Problem Statements, Vision Statements, Ecosystem maps, and RACI matrices
- **📄 Code Generation**: Advanced code editor with AI-powered code review, modification, and debugging capabilities
- **🏞️ Image Generation**: Create images from text prompts using DALL-E 3 with gallery management
- **🎤 Voice Chat**: Voice-to-text transcription and text-to-speech responses for hands-free interaction
- **📚 RAG Integration**: Retrieval Augmented Generation using "The Pragmatic Programmer" PDF with embeddings

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom components
- **AI Services**: OpenAI GPT models, DALL-E 3, Whisper, Google Gemini
- **Audio Processing**: Google Text-to-Speech (gTTS), Pygame
- **Document Processing**: PyPDF2, PDF2Image
- **Machine Learning**: scikit-learn for embeddings and similarity search
- **Deployment**: Docker with multi-stage builds

## 📋 Requirements

- Python 3.12+
- Docker (recommended for deployment)
- API keys for OpenAI and/or Google Gemini
- Microphone access (for voice chat features)

## 🚀 Quick Start

### 1. Environment Setup

Create a `.env` file in the project root with the following variables:

```env
# Required: OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE_URL=https://api.openai.com/v1
OPENAI_API_MODEL=gpt-4

# Optional: Google Gemini Configuration (alternative to OpenAI)
GEMINI_API_KEY=your_gemini_api_key_here
USE_GEMINI=false

# Optional: Custom OpenAI-compatible endpoint
# OPENAI_API_BASE_URL=https://your-custom-endpoint.com/v1
```

### 2. Docker Deployment (Recommended)

#### Standard Build
```bash
docker build -t duckyai .
docker run -p 8501:8501 --env-file .env duckyai
```

#### Multi-Platform Build (Windows/Cross-platform)
```bash
# Create multi-platform builder
docker buildx create --use --name multi-platform-builder
docker buildx inspect --bootstrap

# Build for multiple platforms
docker buildx build -t duckyai --platform linux/amd64,linux/arm64 .

# Run the container
docker run -p 8501:8501 --env-file .env --name duckyai duckyai
```

### 3. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run 🏠_Home.py
```

### 4. Access the Application

Open your browser and navigate to: **http://localhost:8501**

## 🏗️ Project Structure

```
DuckyAI/
├── 🏠_Home.py                 # Main application entry point
├── pages/                     # Streamlit pages
│   ├── 1_💬_Quick_Chat.py     # Chat interface with RAG
│   ├── 2_🎓_Learning_Topics.py # Educational content generation
│   ├── 3_📓_Requirements.py    # Requirements document generation
│   ├── 4_📄_Generate_Code.py   # Code editor and AI assistance
│   ├── 5_🏞️_Images.py         # Image generation and gallery
│   └── 6_🎤_Voice_Chat.py      # Voice interaction interface
├── services/                  # Core business logic
│   ├── llm.py                # OpenAI integration
│   ├── gemini_llm.py         # Google Gemini integration
│   ├── llm_switcher.py       # AI service selection
│   ├── rag.py                # Retrieval Augmented Generation
│   ├── images.py             # Image generation and management
│   ├── audio.py              # Speech processing
│   └── prompts.py            # AI prompt templates
├── helpers/                   # Utility functions
│   ├── sidebar.py            # Shared sidebar component
│   └── util.py               # Common utilities
├── data/                     # Data files and embeddings
│   ├── ThePragmaticProgrammer.pdf
│   ├── ThePragmaticProgrammer.embeddings.csv
│   └── audio/                # Generated audio files
└── static/                   # Static assets
    └── logo.png
```

## 🔧 Configuration Options

### AI Service Selection
DuckyAI uses a wrapper service (`llm_switcher.py`) to seamlessly switch between OpenAI and Google Gemini APIs:

- **OpenAI (Default)**: Full feature support including image generation and voice processing
- **Google Gemini**: Text-based features only (chat, learning, requirements, code generation)
- Set `USE_GEMINI=true` to use Google Gemini instead of OpenAI

**⚠️ Feature Limitations by Model:**
- **Image Generation** (🏞️): Only available with OpenAI (DALL-E 3)
- **Voice Chat** (🎤): Only available with OpenAI (Whisper for transcription)
- **Text Features**: Supported by both OpenAI and Gemini (chat, learning, requirements, code generation)

### Custom OpenAI Endpoints
- Configure `OPENAI_API_BASE_URL` for custom or local OpenAI-compatible APIs
- Useful for Azure OpenAI, local models, or other compatible services

### Model Selection
- Set `OPENAI_API_MODEL` to specify which GPT model to use
- Default: `gpt-4` (recommended for best results)

## 🎯 Usage Examples

1. **Quick Development Questions**: Ask coding questions with optional book context
2. **Learning New Technologies**: Generate structured learning materials at your level
3. **Project Planning**: Create professional requirement documents
4. **Code Review**: Upload code for AI-powered review and suggestions
5. **Visual Content**: Generate images for presentations or documentation
6. **Hands-free Coding**: Use voice commands for coding assistance

## 🐳 Docker Notes

- The Dockerfile uses multi-stage builds for optimized image size
- Includes all necessary system dependencies (poppler-utils for PDF processing)
- Exposes port 8501 for Streamlit
- Supports both x86_64 and ARM64 architectures

## 📝 License

This project is part of CS5740 coursework. Please refer to your course guidelines for usage and distribution policies.

## 🤝 Contributing

This is an educational project. For improvements or bug fixes, please follow standard Git workflow practices.

---

**Happy Coding with DuckyAI! 🐥**re 
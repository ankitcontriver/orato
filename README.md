# 🎤 Orato - AI Voice Processing Suite

<div align="center">

![Orato Logo](https://img.shields.io/badge/ORATO-AI%20Voice%20Processing-blue?style=for-the-badge&logo=mic&logoColor=white)

**A stunning, futuristic web-based tool for Speech-to-Text (STT) and Text-to-Speech (TTS) using Azure Cognitive Services and ElevenLabs APIs**

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![ElevenLabs](https://img.shields.io/badge/ElevenLabs-000000?style=flat-square&logo=openai&logoColor=white)](https://elevenlabs.io/)

</div>

## ✨ Features

### 🎯 **Core Functionality**
- **Text-to-Speech (TTS)** - Convert text to natural-sounding speech
- **Speech-to-Text (STT)** - Transcribe audio files to text
- **Batch Processing** - Process multiple files at once
- **Multi-language Support** - 14+ languages including Arabic, Hindi, French, Pashto, Dari, and more

### 🎨 **Stunning UI Design**
- **Futuristic Interface** - Dynamic matrix background effects
- **Minimalistic Design** - Clean, modern, and intuitive
- **Responsive Layout** - Works perfectly on desktop and mobile
- **Real-time Feedback** - Live character counts and progress indicators
- **High-tech Animations** - Smooth transitions and visual effects

### 🔧 **Technical Features**
- **Docker Support** - Single command deployment
- **Modular Architecture** - Loosely coupled components
- **API Integration** - Azure Cognitive Services & ElevenLabs
- **File Management** - Secure upload and download handling
- **Error Handling** - Comprehensive error management
- **Health Checks** - Built-in monitoring

## 🚀 Quick Start

### **Single Docker Command** (Recommended)

```bash
docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/downloads:/app/downloads orato:latest
```

### **Using Docker Compose** (Even Easier)

```bash
# Clone the repository
git clone <repository-url>
cd Orato

# Start the application
docker-compose up -d

# Access the application
open http://localhost:5000
```

### **Manual Setup** (For Development)

```bash
# Clone the repository
git clone <repository-url>
cd Orato

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access the application
open http://localhost:5000
```

## 📋 Prerequisites

- **Docker** (recommended) or **Python 3.11+**
- **API Keys** for Azure Cognitive Services and/or ElevenLabs
- **Modern Web Browser** (Chrome, Firefox, Safari, Edge)

## 🔑 API Keys Setup

### Azure Cognitive Services
1. Go to [Azure Portal](https://portal.azure.com/)
2. Create a Speech Services resource
3. Get your API key and region
4. Use these credentials in the application

### ElevenLabs
1. Sign up at [ElevenLabs](https://elevenlabs.io/)
2. Get your API key from the dashboard
3. Use this credential in the application

## 🌍 Supported Languages

| Language | Code | Azure Support | ElevenLabs Support |
|----------|------|---------------|-------------------|
| English | `en` | ✅ | ✅ |
| Arabic | `ar` | ✅ | ❌ |
| Hindi | `hi` | ✅ | ❌ |
| French | `fr` | ✅ | ❌ |
| Pashto | `ps` | ✅ | ❌ |
| Dari | `prs` | ✅ | ❌ |
| Spanish | `es` | ✅ | ❌ |
| German | `de` | ✅ | ❌ |
| Italian | `it` | ✅ | ❌ |
| Portuguese | `pt` | ✅ | ❌ |
| Russian | `ru` | ✅ | ❌ |
| Japanese | `ja` | ✅ | ❌ |
| Korean | `ko` | ✅ | ❌ |
| Chinese | `zh` | ✅ | ❌ |

## 📖 Usage Guide

### **Text-to-Speech (TTS)**

1. **Select Provider**: Choose between Azure or ElevenLabs
2. **Enter Text**: Type or paste your text
3. **Choose Language**: Select from 14+ supported languages
4. **Select Voice**: Pick a specific voice or use auto-select
5. **Enter API Key**: Provide your provider's API key
6. **Generate**: Click "Generate Speech" and download the audio

### **Speech-to-Text (STT)**

1. **Upload Audio**: Drag and drop or click to select an audio file
2. **Choose Language**: Select the language of your audio
3. **Enter API Key**: Provide your Azure API key
4. **Process**: Click "Process Audio" to get the transcription

### **Batch Processing**

1. **Prepare JSON File**: Create a JSON file with key-value pairs
   ```json
   {
     "1.wav": "Hello, this is sample text 1",
     "2.wav": "Hello, this is sample text 2",
     "3.wav": "Hello, this is sample text 3"
   }
   ```
2. **Upload File**: Select your JSON file
3. **Configure Settings**: Choose provider, language, and API key
4. **Process**: Click "Process Batch" to generate all audio files

## 🏗️ Architecture

### **Modular Design**

```
Orato/
├── app.py                 # Main Flask application
├── services/              # Service layer
│   ├── azure_service.py   # Azure TTS/STT integration
│   ├── elevenlabs_service.py # ElevenLabs TTS integration
│   ├── batch_service.py   # Batch processing logic
│   └── file_service.py    # File management
├── utils/                 # Utility functions
│   └── config.py         # Configuration management
├── templates/             # HTML templates
│   └── index.html        # Main UI template
├── static/               # Static assets
│   ├── style.css         # Futuristic CSS styles
│   └── script.js         # Interactive JavaScript
├── uploads/              # Temporary upload directory
├── downloads/            # Generated files directory
└── Dockerfile           # Docker configuration
```

### **Component Separation**

- **Azure Service**: Handles all Azure Cognitive Services operations
- **ElevenLabs Service**: Manages ElevenLabs API interactions
- **Batch Service**: Processes multiple files efficiently
- **File Service**: Handles file uploads, downloads, and cleanup
- **Config Utils**: Centralized configuration management

## 🐳 Docker Configuration

### **Dockerfile Features**
- **Multi-stage build** for optimized image size
- **Health checks** for container monitoring
- **Security hardening** with non-root user
- **Efficient caching** with layered approach

### **Docker Compose Features**
- **Volume mounting** for persistent data
- **Environment variables** for configuration
- **Health monitoring** with automatic restart
- **Port mapping** for easy access

## 🔧 Configuration

### **Environment Variables**

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# File Upload Settings
MAX_FILE_SIZE=52428800  # 50MB
ALLOWED_EXTENSIONS=wav,mp3,mp4,m4a,ogg,flac,json
```

### **Customization**

You can customize the application by modifying:
- **Languages**: Add new languages in `utils/config.py`
- **Voices**: Update voice mappings in service files
- **UI**: Modify CSS and JavaScript in `static/` directory
- **API Endpoints**: Extend functionality in `app.py`

## 🚨 Troubleshooting

### **Common Issues**

1. **Docker Build Fails**
   ```bash
   # Clean Docker cache
   docker system prune -a
   # Rebuild
   docker-compose build --no-cache
   ```

2. **API Key Errors**
   - Verify your API key is correct
   - Check if the key has proper permissions
   - Ensure the service region matches

3. **File Upload Issues**
   - Check file size limits (50MB max)
   - Verify file format is supported
   - Ensure proper permissions on upload directory

4. **Audio Generation Fails**
   - Verify text is not empty
   - Check language and voice compatibility
   - Ensure API quota is not exceeded

### **Logs and Debugging**

```bash
# View application logs
docker-compose logs -f orato

# Check container health
docker-compose ps

# Access container shell
docker-compose exec orato bash
```

## 📊 Performance

### **Optimizations**
- **Async Processing** for better responsiveness
- **File Cleanup** to prevent disk space issues
- **Connection Pooling** for API efficiency
- **Caching** for voice lists and configurations

### **Scaling**
- **Horizontal Scaling** with multiple containers
- **Load Balancing** for high availability
- **Database Integration** for production use
- **CDN Integration** for static assets

## 🔒 Security

### **Security Features**
- **Input Validation** for all user inputs
- **File Type Verification** for uploads
- **API Key Protection** with secure handling
- **CORS Configuration** for cross-origin requests
- **Rate Limiting** to prevent abuse

### **Best Practices**
- Use environment variables for sensitive data
- Regularly update dependencies
- Monitor API usage and costs
- Implement proper logging and monitoring

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**

```bash
# Clone repository
git clone <repository-url>
cd Orato

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Azure Cognitive Services** for speech processing capabilities
- **ElevenLabs** for high-quality voice synthesis
- **Flask** for the web framework
- **Docker** for containerization
- **Open Source Community** for inspiration and support

## 📞 Support

- **Documentation**: [Full Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: support@orato.ai

---

<div align="center">

**Made with ❤️ for the AI community**

[![GitHub stars](https://img.shields.io/github/stars/your-repo/orato?style=social)](https://github.com/your-repo/orato)
[![GitHub forks](https://img.shields.io/github/forks/your-repo/orato?style=social)](https://github.com/your-repo/orato)

</div>

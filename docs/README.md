# Email Guard - AI-Powered Email Security Analysis

A comprehensive web application that analyzes email content using multiple AI and ML models to detect phishing, spam, and other security threats. The system provides real-time analysis with detailed results and maintains a secure, scalable architecture.

## 🚀 Features

- **Multi-Model AI Analysis**: Uses multiple AI/ML models including DistilBERT, phishing-detection-py, and rule-based analyzers
- **JWT Authentication**: Secure token-based authentication with HTTP-only cookies
- **Real-time Analysis**: Instant email content analysis with detailed confidence scores
- **History Tracking**: Maintains analysis history for each authenticated user
- **Modern React Frontend**: Clean, responsive UI with TypeScript and Vite
- **APISIX API Gateway**: Production-ready gateway with rate limiting and load balancing
- **Docker Deployment**: Containerized architecture for easy deployment and scaling
- **Comprehensive Security**: Multiple layers of security including input validation, rate limiting, and container isolation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  React Frontend │    │  APISIX Gateway │    │  FastAPI Backend│
│  (Vercel)       │    │  (Port 9080)    │    │  (Port 8000)    │
│                 │    │                 │    │                 │
│ - Authentication│◄──►│  - Rate Limiting│◄──►│  - JWT Auth     │
│ - Email Scanner │    │  - Load Balance │    │  - Input Verify │
│ - Dashboard     │    │  - SSL/TLS      │    │  - AI Analysis  │
│ - History View  │    │  - CORS         │    │  - Model Loading│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                              ┌─────────────────┐
                                              │   AI Models     │
                                              │                 │
                                              │ - HuggingFace   │
                                              │ - DistilBERT    │
                                              │ - Rule-based    │
                                              │ - phishing-py   │
                                              └─────────────────┘
```

## 📊 User Journey

1. **Authentication**: User enters purchased token on auth page
2. **Token Validation**: APISIX gateway validates token and creates secure JWT
3. **Model Status Check**: Frontend verifies AI models are loaded and ready
4. **Email Analysis**: User submits email content for multi-model analysis
5. **AI Processing**: Backend processes email through multiple AI models in parallel
6. **Results Display**: Dashboard shows detailed analysis results with confidence scores
7. **History Tracking**: Analysis results are saved for future reference

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework with automatic API documentation
- **JWT**: JSON Web Tokens for secure authentication
- **Transformers**: Hugging Face ML models for advanced text analysis
- **Pydantic**: Data validation and serialization
- **Uvicorn**: High-performance ASGI server
- **phishing-detection-py**: Specialized phishing detection library

### Frontend
- **React 19**: Latest React with TypeScript for type safety
- **Vite**: Fast build tool and development server
- **Axios**: HTTP client with timeout and error handling
- **Tailwind CSS**: Utility-first CSS framework for modern styling
- **TypeScript**: Static type checking for better code quality

### Infrastructure
- **APISIX**: API Gateway for routing, rate limiting, and load balancing
- **Docker**: Containerization for consistent deployment
- **etcd**: Configuration storage for APISIX
- **Vercel**: Frontend deployment platform
- **Render**: Backend deployment platform (optional)

### AI/ML Models
- **cybersectony/phishing-email-detection-distilbert_v2.1**: Advanced phishing detection
- **aamoshdahal/email-phishing-distilbert-finetuned**: Email-specific DistilBERT model
- **phishing-detection-py**: PyPI package for URL analysis
- **Rule-based Analysis**: Pattern matching and heuristic analysis

## 🔧 Environment Variables

### Backend Service
```bash
# Required
JWT_SECRET_KEY=your-super-secure-jwt-secret-key-here

# Optional
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Frontend Service
```bash
# Required for production
VITE_API_URL=http://localhost:9080

# Optional
VITE_APP_TITLE=Email Guard
```

### APISIX Service
```bash
# Optional (has secure defaults)
ADMIN_KEY=edd1c9f034335f136f87ad84b625c8f1
```

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose**: For containerized deployment
- **Node.js 18+**: For frontend development
- **Python 3.11+**: For backend development
- **Git**: For cloning and model management

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/email-guard.git
cd email-guard

# Start with convenience script
chmod +x run-docker.sh
./run-docker.sh setup

# Or manually
cd docker
docker-compose up -d --build
./setup-apisix.sh
cd ..
```

**Access Points:**
- **API Gateway**: http://localhost:9080
- **APISIX Admin**: http://localhost:9180
- **Backend Direct**: http://localhost:8000

### Option 2: Local Development

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
export JWT_SECRET_KEY="your-secret-key"
python app.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Option 3: Lightweight Version

For simpler deployment needs, check out our lightweight version with fewer dependencies:
**[Email Guard Lightweight](https://github.com/Richdale04/Email-Guard-Lightweight)**

Features of the lightweight version:
- **Simplified Architecture**: Single backend service
- **Replit Compatible**: Can be deployed on Replit
- **Minimal Dependencies**: Reduced resource requirements
- **Essential Features**: Core email analysis functionality
- **Faster Deployment**: Quick setup for testing and development

## 📡 API Endpoints

### Authentication
- `POST /auth/token` - Authenticate with purchased token
- `POST /auth/logout` - Logout and clear authentication cookie

### Email Analysis
- `POST /scan/email` - Analyze email content with multiple models
- `GET /models/status` - Check AI model loading status

### Data Management
- `GET /history` - Get analysis history for authenticated user
- `GET /health` - System health check

### Request/Response Examples

**Authentication:**
```json
POST /auth/token
{
  "token": "sample_token_1"
}

Response:
{
  "message": "Authentication successful",
  "user": {
    "sub": "user1",
    "role": "user"
  }
}
```

**Email Analysis:**
```json
POST /scan/email
{
  "email_text": "Urgent: Your account will be suspended unless you verify immediately..."
}

Response:
{
  "results": [
    {
      "model_source": "HuggingFace",
      "model_name": "cybersectony-distilbert",
      "decision": "phishing",
      "confidence": 0.94,
      "description": "High probability phishing email detected"
    },
    {
      "model_source": "PyPI",
      "model_name": "phishing-detection-py",
      "decision": "phishing",
      "confidence": 0.87,
      "description": "Suspicious URL patterns detected"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z",
  "email_snippet": "Urgent: Your account will be suspended..."
}
```

## 🔒 Security Features

### Authentication & Authorization
- **JWT Tokens**: Secure authentication with configurable expiration
- **HTTP-Only Cookies**: XSS protection through secure cookie storage
- **Role-Based Access**: User and admin roles with different permissions
- **Token Validation**: Server-side verification on all protected endpoints

### Rate Limiting & Protection
- **APISIX Rate Limiting**: Prevents API abuse and brute force attacks
  - Authentication: 5 requests/7 minutes per IP
  - Scanning: 20 requests/minute per IP
  - History: 30 requests/minute per IP
- **Input Validation**: Comprehensive input sanitization and validation
- **Request Size Limits**: Prevents DoS attacks through large payloads

### Data Security
- **Temporary Storage**: Email content stored only during analysis
- **No PII Collection**: Minimal personal data collection
- **Secure Headers**: Comprehensive HTTP security headers
- **Container Isolation**: Docker-based service isolation

### Infrastructure Security
- **Container Security**: Official base images with minimal attack surface
- **Network Isolation**: Internal Docker networks for service communication
- **Secret Management**: Environment variable-based configuration
- **Health Monitoring**: Continuous service health checking

## 📈 Performance & Scaling

### Model Loading
- **Background Loading**: Models load asynchronously during startup
- **Status Monitoring**: Real-time model readiness checking
- **Graceful Degradation**: Fallback to rule-based analysis if models fail
- **Cold Start Handling**: Extended timeouts for initial model loading

### Rate Limiting
- **Tiered Limits**: Different limits for different endpoint types
- **Burst Protection**: Handles traffic spikes gracefully
- **IP-Based**: Per-client rate limiting
- **Production Ready**: Redis backend support for scaling

### Deployment Options
- **Docker**: Full containerized deployment
- **Kubernetes**: Orchestration support for large deployments
- **Cloud Platforms**: Vercel (frontend) + Render/AWS (backend)
- **Local Development**: Direct execution for development

## 📋 Test Tokens

For development and testing:

```bash
# User tokens
sample_token_1  # Standard user access
sample_token_2  # Admin user access

# Usage in API calls
curl -X POST http://localhost:9080/auth/token \
  -H "Content-Type: application/json" \
  -d '{"token": "sample_token_1"}'
```

## 🔧 Configuration

### Rate Limiting Configuration
```yaml
# APISIX Rate Limiting
authentication_endpoints:
  rate: 5 requests per 7 minutes
  burst: 10 requests
  
scan_endpoints:
  rate: 20 requests per minute
  burst: 30 requests
  timeout: 300 seconds
  
history_endpoints:
  rate: 30 requests per minute
  burst: 50 requests
```

### Model Configuration
```python
# Available Models
models = [
    "cybersectony/phishing-email-detection-distilbert_v2.1",
    "aamoshdahal/email-phishing-distilbert-finetuned",
    "phishing-detection-py",
    "rule-based-analyzer"
]
```

## 🐛 Troubleshooting

### Common Issues

**Models Not Loading:**
```bash
# Check model status
curl http://localhost:9080/models/status

# View backend logs
docker-compose logs backend

# Manual model loading
docker-compose exec backend python -c "
from ai.email_guard import get_analyzer
analyzer = get_analyzer()
print(f'Models loaded: {len(analyzer.analyzers)}')
"
```

**CORS Errors:**
```bash
# Check frontend environment
echo $VITE_API_URL

# Verify APISIX CORS config
curl http://localhost:9080/health \
  -H "Origin: http://localhost:5173"
```

**Rate Limiting Issues:**
```bash
# Check current limits
curl http://localhost:9180/apisix/admin/routes \
  -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'
```

### Debug Commands
```bash
# Service status
./run-docker.sh status

# View logs
./run-docker.sh logs

# Test connectivity
curl http://localhost:9080/health
curl http://localhost:8000/health
```

## 📚 Documentation

- **[Docker Setup](docker/DOCKER_README.md)**: Complete Docker deployment guide
- **[Security Notes](docs/security_notes.md)**: Comprehensive security documentation
- **[AI Models](ai/README.md)**: AI model architecture and usage
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)**: Production deployment instructions

## 🚀 Deployment

### Production Deployment

#### Frontend (Vercel)
```bash
# Connect GitHub repository to Vercel
# Set environment variables:
VITE_API_URL=https://your-api-domain.com

# Deploy automatically on push to main
```

#### Backend (Docker/Cloud)
```bash
# Set production environment variables
export JWT_SECRET_KEY="super-secure-production-key"
export CORS_ORIGINS="https://your-frontend-domain.com"

# Deploy with Docker
docker-compose -f docker-compose.prod.yml up -d
```

#### Lightweight Alternative
For simpler deployments, use the [Email Guard Lightweight](https://github.com/Richdale04/Email-Guard-Lightweight) version which:
- Runs on Replit with minimal setup
- Has reduced dependencies
- Provides core functionality
- Suitable for testing and small deployments

## 🧪 Testing

### Manual Testing
```bash
# Test authentication
curl -X POST http://localhost:9080/auth/token \
  -H "Content-Type: application/json" \
  -d '{"token": "sample_token_1"}'

# Test email analysis
curl -X POST http://localhost:9080/scan/email \
  -H "Content-Type: application/json" \
  -b "auth_token=your-jwt-token" \
  -d '{"email_text": "Test phishing email content"}'
```

### Sample Test Emails
- **Phishing**: "URGENT: Your account has been suspended. Click here to verify immediately..."
- **Spam**: "CONGRATULATIONS! You've won $1,000,000! Click here to claim..."
- **Safe**: "Hi John, Thanks for your email regarding the meeting. Best regards, Sarah"

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with proper testing
4. **Add tests** for new functionality
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Submit a Pull Request**

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add type hints for all functions
- Include comprehensive error handling
- Write tests for new features
- Update documentation for changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

### Getting Help
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check the docs/ directory
- **Security Issues**: Contact security@emailguard.com

### Commercial Support
For enterprise deployments and commercial support:
- **Email**: support@emailguard.com
- **Documentation**: Available in the docs/ directory
- **Consulting**: Custom deployment and integration services

## 🗺️ Roadmap

### Current Version (v1.0)
- ✅ Multi-model AI analysis
- ✅ JWT authentication
- ✅ Docker deployment
- ✅ Rate limiting
- ✅ Modern React frontend

### Upcoming Features (v1.1)
- [ ] Additional ML models
- [ ] Real-time threat intelligence
- [ ] Advanced analytics dashboard
- [ ] API rate limiting improvements
- [ ] Enhanced security features

### Future Plans (v2.0)
- [ ] Mobile application
- [ ] Enterprise SSO integration
- [ ] Multi-language support
- [ ] Advanced reporting features
- [ ] Machine learning model training interface

## 📊 Performance Metrics

### Typical Response Times
- **Authentication**: < 100ms
- **Email Analysis**: 2-5 seconds (first request), < 1 second (subsequent)
- **History Retrieval**: < 200ms
- **Model Status Check**: < 50ms

### Supported Load
- **Concurrent Users**: 100+ (with proper scaling)
- **Requests per Minute**: 1000+ (with rate limiting)
- **Email Size**: Up to 10,000 characters
- **Model Accuracy**: 85-95% depending on content type

---

**Email Guard** - Protecting organizations from email-based threats through advanced AI analysis and comprehensive security measures.

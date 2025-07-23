# Email Guard - AI-Powered Email Security Analysis

A comprehensive web application that analyzes email content using multiple AI and ML models to detect phishing, spam, and other security threats.

## Features

- **Multi-Model Analysis**: Uses multiple AI/ML models for comprehensive email analysis
- **JWT Authentication**: Secure token-based authentication with rate limiting
- **Real-time Analysis**: Instant email content analysis with detailed results
- **History Tracking**: Maintains analysis history for each user
- **Modern UI**: Clean, responsive React frontend with intuitive design
- **API Gateway Ready**: Designed to work with APISIX gateway for production deployment

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  React Frontend │    │  APISIX Gateway │    │  FastAPI Backend│
│                 │    │                 │    │                 │
│ - Authentication│◄──►│  - Rate Limiting│◄──►│  - JWT Auth     │
│ - Email Scanner │    │  - Load Balance │    │  - Input Verify │
│ - Dashboard     │    │  - SSL/TLS      │    │  - AI Analysis  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                              ┌─────────────────┐
                                              │   AI Models     │
                                              │                 │
                                              │  - DistilBERT   │
                                              │  - Rule-based   │
                                              │  - Custom ML    │
                                              └─────────────────┘
```

## User Journey

1. **Authentication**: User enters purchased token on auth page
2. **Token Validation**: APISIX gateway validates token and creates JWT
3. **Email Analysis**: User submits email content for analysis
4. **Multi-Model Processing**: Backend processes email through multiple AI models
5. **Results Display**: Dashboard shows analysis results and history

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **JWT**: JSON Web Tokens for authentication
- **Transformers**: Hugging Face ML models
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **React 19**: Modern React with TypeScript
- **Vite**: Fast build tool
- **Axios**: HTTP client
- **CSS3**: Modern styling with gradients and animations

### AI/ML
- **DistilBERT**: Pre-trained models for email classification
- **Rule-based Analysis**: Fallback analysis system
- **Custom Models**: Extensible model architecture

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Backend Setup

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python app.py
   ```
   
   Or with Docker:
   ```bash
   docker build -t email-guard-backend .
   docker run -p 8000:8000 email-guard-backend
   ```

### Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

## API Endpoints

### Authentication
- `POST /auth/token` - Authenticate with token
- `GET /health` - Health check

### Email Analysis
- `POST /scan/email` - Analyze email content
- `GET /history` - Get analysis history

### Request/Response Examples

**Authenticate**:
```json
POST /auth/token
{
  "token": "your_purchased_token"
}
```

**Analyze Email**:
```json
POST /scan/email
{
  "email_text": "Your email content here..."
}
```

**Response**:
```json
{
  "results": [
    {
      "model_source": "huggingface",
      "model_name": "distilbert-phishing",
      "decision": "phishing",
      "confidence": 0.85,
      "description": "Model prediction: phishing with 85% confidence"
    }
  ],
  "timestamp": "2024-01-01T12:00:00Z",
  "email_snippet": "Email preview..."
}
```

## Configuration

### Environment Variables
```bash
# JWT Configuration
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# API Configuration
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Token Management
Tokens are stored in `backend/tokens.csv`:
```csv
token,sub,role,expires_at
sample_token_1,user1,user,2024-12-31
sample_token_2,user2,admin,2024-12-31
```

## Security Features

- **Rate Limiting**: 5 authentication requests per 7 minutes per IP
- **Input Sanitization**: Comprehensive email content validation
- **JWT Tokens**: Secure HTTP-only cookies
- **CORS Protection**: Configured origins only
- **Input Validation**: Pydantic models for all inputs

## AI Models

### Available Models
1. **DistilBERT Models**:
   - `aamoshdahal-email-phishing-distilbert-finetuned`
   - `cybersectony-phishing-email-detection-distilbert_v2.1`

2. **Rule-based Analysis**:
   - Pattern matching for common threats
   - Metadata analysis
   - Risk scoring

### Adding New Models
1. Place model files in `ai/models/`
2. Update `EmailAnalyzer.load_models()` in `ai/email_guard.py`
3. Model should return standardized results

## Production Deployment

### With APISIX Gateway
1. **Configure APISIX**:
   ```yaml
   routes:
     - uri: /auth/*
       upstream:
         type: roundrobin
         nodes:
           "backend:8000": 1
       plugins:
         rate-limit:
           rate: 5
           burst: 10
           time_window: 420
   ```

2. **SSL/TLS**: Configure certificates in APISIX
3. **Load Balancing**: Multiple backend instances
4. **Monitoring**: Health checks and metrics

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your-secret-key
    volumes:
      - ./backend/scan_history:/app/backend/scan_history

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Sample Test Emails
- **Phishing**: Account suspension with urgent action required
- **Spam**: Promotional offers with suspicious links
- **Safe**: Normal business communication

## Troubleshooting

### Common Issues

1. **CORS Errors**: Check CORS configuration in backend
2. **Model Loading**: Ensure model files are in correct location
3. **Authentication**: Verify token format and expiration
4. **Rate Limiting**: Wait 7 minutes between auth attempts

### Logs
- Backend logs: Check uvicorn output
- Frontend logs: Browser developer console
- Model logs: Check AI model loading messages

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review troubleshooting section

## Roadmap

- [ ] Additional ML models
- [ ] Real-time threat intelligence
- [ ] Advanced analytics dashboard
- [ ] API rate limiting improvements
- [ ] Mobile application
- [ ] Enterprise features

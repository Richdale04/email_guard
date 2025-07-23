# Email Guard - Deployment Guide

This guide explains how to deploy the Email Guard application for both local development and production environments.

## ⚠️ Important Notice: Architecture Complexity

**This full-featured version of Email Guard is designed for local deployment and enterprise environments.** The application architecture includes:

- **Multiple AI/ML Models**: DistilBERT models, rule-based analysis, and custom ML models
- **APISIX API Gateway**: Advanced rate limiting, load balancing, and security features
- **Docker Containerization**: Multi-container setup with etcd storage
- **Complex Dependencies**: Transformers, PyTorch, and large model files

**For free-tier deployment services (Render, Railway, etc.), this architecture is too resource-intensive.**

### Why This Architecture is Complex

The current implementation includes:
- **Large ML Models**: DistilBERT models require significant memory (2-4GB per model)
- **APISIX Gateway**: Enterprise-grade API gateway with etcd dependency
- **Multiple Containers**: Backend, APISIX, etcd, and model loading services
- **Real-time Model Loading**: Models are loaded into memory during startup

**This project is tested and optimized for local deployment. For public online deployment, you only need to copy the backend services (FastAPI, Docker, AI folders) to your server, run docker-compose to initiate services and configuration, then use the server endpoint in the environment variable of the React Frontend called `VITE_API_URL`.**

## Recommended Deployment Strategy

### Option 1: Local Development (Recommended)
- **Use Case**: Development, testing, personal use
- **Setup**: Docker Compose with APISIX gateway
- **Resources**: Requires 4GB+ RAM, 10GB+ storage

### Option 2: Production Server Deployment
- **Use Case**: Public online deployment
- **Setup**: VPS/Cloud server with Docker
- **Resources**: 2GB+ RAM, 20GB+ storage

### Option 3: Lightweight Version
- **Use Case**: Free-tier deployment services
- **Alternative**: [Email-Guard-Lightweight](https://github.com/Richdale04/Email-Guard-Lightweight)
- **Features**: Simplified backend, Replit-compatible, fewer AI models

## Local Development Setup

### Prerequisites
- Docker & Docker Compose
- 4GB+ RAM available
- 20GB+ free disk space

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/email-guard.git
   cd email-guard
   ```

2. **Start all services**:
   ```bash
   cd docker
   ./run-docker.sh setup
   ```

3. **Access the application**:
   - Frontend: http://localhost:5173
   - API Gateway: http://localhost:9080
   - Backend: http://localhost:8000

## Environment Variables

### Frontend (React/Vite)
```bash
# .env file in frontend directory
VITE_API_URL=http://localhost:9080  # Points to APISIX gateway
```

### Backend (FastAPI)
```bash
# Environment variables for backend container
SECRET_KEY=your-super-secret-key-change-this
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
LOG_LEVEL=INFO
```

### APISIX Gateway
```bash
# APISIX configuration (in apisix-config.yaml)
ADMIN_KEY=edd1c9f034335f136f87ad84b625c8f1
NODE_LISTEN=9080
ADMIN_LISTEN=9180
ETCD_HOST=etcd
ETCD_PORT=2379
```

### Docker Services (docker-compose.yml)
```bash
# Backend service
SECRET_KEY=your-super-secret-key-change-this
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# APISIX service
ADMIN_KEY=edd1c9f034335f136f87ad84b625c8f1
NODE_LISTEN=9080
ADMIN_LISTEN=9180

# ETCD service
ETCD_HOST=etcd
ETCD_PORT=2379
```

### AI Models Configuration
```bash
# Model loading configuration (in ai/email_guard.py)
MODELS_DIR=/app/ai/models/
ML_AVAILABLE=True
PHISHING_DETECTOR_AVAILABLE=True
```

## Production Server Deployment

### Server Requirements
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **RAM**: 2GB+ (4GB recommended)
- **Storage**: 20GB+ (for models and data)
- **CPU**: 2+ cores

### Deployment Steps

1. **Prepare the server**:
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **Deploy the application**:
   ```bash
   # Clone repository
   git clone https://github.com/your-username/email-guard.git
   cd email-guard
   
   # Copy backend services to server
   cp -r backend/ /opt/email-guard/
   cp -r ai/ /opt/email-guard/
   cp -r docker/ /opt/email-guard/
   
   # Navigate to deployment directory
   cd /opt/email-guard/docker
   ```

3. **Configure environment variables**:
   ```bash
   # Create environment file
   cat > .env << EOF
   SECRET_KEY=$(openssl rand -hex 32)
   CORS_ORIGINS=https://your-frontend-domain.com
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ADMIN_KEY=$(openssl rand -hex 32)
   EOF
   ```

4. **Start services**:
   ```bash
   # Build and start
   docker-compose up -d --build
   
   # Configure APISIX routes
   chmod +x setup-apisix.sh
   ./setup-apisix.sh
   ```

5. **Configure frontend**:
   ```bash
   # Set VITE_API_URL to your server endpoint
   # Example: VITE_API_URL=https://your-server-ip:9080
   ```

### Production Environment Variables

#### Backend Container
```bash
SECRET_KEY=your-super-secret-key-change-this
CORS_ORIGINS=https://your-frontend-domain.com
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
LOG_LEVEL=INFO
```

#### APISIX Gateway
```bash
ADMIN_KEY=your-apisix-admin-key
NODE_LISTEN=9080
ADMIN_LISTEN=9180
ETCD_HOST=etcd
ETCD_PORT=2379
```

#### Frontend (Vercel/Netlify)
```bash
VITE_API_URL=https://your-server-ip:9080
```

## Frontend Deployment (Vercel/Netlify)

### Vercel Deployment

1. **Connect repository**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Set root directory to `frontend`

2. **Configure environment variables**:
   ```
   VITE_API_URL=https://your-backend-server:9080
   ```

3. **Build settings**:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

### Netlify Deployment

1. **Connect repository**:
   - Go to [netlify.com](https://netlify.com)
   - Connect your GitHub repository
   - Set build directory to `frontend`

2. **Configure environment variables**:
   ```
   VITE_API_URL=https://your-backend-server:9080
   ```

3. **Build settings**:
   - Build Command: `cd frontend && npm run build`
   - Publish Directory: `frontend/dist`

## Service Management

### Using Convenience Scripts
```bash
# Start all services
./run-docker.sh up

# Stop all services
./run-docker.sh down

# View logs
./run-docker.sh logs

# Check status
./run-docker.sh status

# Restart services
./run-docker.sh restart
```

### Manual Commands
```bash
# Navigate to docker directory
cd docker

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild services
docker-compose up -d --build
```

## Monitoring and Health Checks

### Health Check Endpoints
- **Backend**: `GET /health`
- **APISIX**: `GET /apisix/admin/services`
- **Models Status**: `GET /models/status`
- **Frontend**: Built-in Vite dev server health

### Log Monitoring
```bash
# Backend logs
docker-compose logs -f backend

# APISIX logs
docker-compose logs -f apisix

# All services
docker-compose logs -f
```

### Performance Monitoring
- **APISIX Metrics**: Available at `/apisix/admin/metrics`
- **Backend Metrics**: Built-in FastAPI metrics
- **Resource Usage**: `docker stats`

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check port usage
   sudo netstat -tulpn | grep :9080
   
   # Change ports in docker-compose.yml if needed
   ```

2. **Model Loading Issues**
   ```bash
   # Check model files
   docker-compose exec backend ls -la /app/ai/models/
   
   # Rebuild models
   docker-compose down
   docker-compose up -d --build
   ```

3. **APISIX Configuration Issues**
   ```bash
   # Reconfigure APISIX
   ./setup-apisix.sh
   
   # Check routes
   curl http://localhost:9180/apisix/admin/routes
   ```

4. **CORS Errors**
   - Verify `CORS_ORIGINS` environment variable
   - Check frontend `VITE_API_URL` setting
   - Ensure APISIX CORS plugin is configured

### Debug Commands
```bash
# Test backend health
curl http://localhost:8000/health

# Test APISIX gateway
curl http://localhost:9080/health

# Test models status
curl http://localhost:9080/models/status

# Test authentication
curl -X POST http://localhost:9080/auth/token \
  -H "Content-Type: application/json" \
  -d '{"token": "sample_token_1"}'

# Check APISIX routes
curl http://localhost:9180/apisix/admin/routes
```

## Security Considerations

### Production Security
1. **Change default secrets**:
   - `SECRET_KEY` for JWT
   - `ADMIN_KEY` for APISIX
   - Database passwords

2. **Network security**:
   - Use HTTPS with SSL certificates
   - Configure firewall rules
   - Restrict admin access

3. **Container security**:
   - Regular base image updates
   - Non-root user execution
   - Resource limits

### Rate Limiting
APISIX provides built-in rate limiting:
- **Authentication**: 5 requests per 7 minutes per IP
- **Scanning**: 20 requests per minute per IP
- **History**: 30 requests per minute per IP
- **Models Status**: 60 requests per minute per IP

## Cost Optimization

### Resource Requirements
- **Development**: 4GB RAM, 10GB storage
- **Production**: 2GB+ RAM, 20GB+ storage
- **Bandwidth**: Depends on usage patterns

### Scaling Considerations
- **Horizontal scaling**: Multiple backend instances
- **Load balancing**: APISIX handles distribution
- **Caching**: Redis for session management
- **CDN**: For static frontend assets

## Alternative: Lightweight Version

For free-tier deployment services, use the lightweight version:
- **Repository**: [Email-Guard-Lightweight](https://github.com/Richdale04/Email-Guard-Lightweight)
- **Features**: Simplified backend, Replit-compatible, fewer AI models
- **Deployment**: Works on Render, Railway, Replit free tiers
- **Trade-offs**: Fewer AI models, basic rate limiting, no APISIX gateway

## Support and Maintenance

### Regular Maintenance
1. **Update dependencies**: Monthly security updates
2. **Monitor logs**: Check for errors and performance issues
3. **Backup data**: Regular backups of scan history
4. **Security patches**: Keep Docker images updated

### Getting Help
- **Issues**: Create GitHub issues for bugs
- **Documentation**: Check project README files
- **Community**: Join project discussions
- **Security**: Report security issues privately

## Next Steps

1. **Database**: Add PostgreSQL for persistent data
2. **Caching**: Implement Redis for session management
3. **Monitoring**: Set up comprehensive monitoring
4. **SSL**: Configure HTTPS certificates
5. **Backup**: Implement automated backup strategy
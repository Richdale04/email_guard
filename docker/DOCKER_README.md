# Email Guard - Docker Setup with APISIX

This document explains how to run the Email Guard application using Docker with APISIX as the API gateway for rate limiting and routing.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  APISIX Gateway │    │  FastAPI Backend│    │  etcd          │
│  Port: 9080     │    │  Port: 8000     │    │  Port: 2379    │
│                 │    │                 │    │                 │
│ - Rate Limiting │◄──►│  - JWT Auth     │    │ - Configuration │
│ - Load Balance  │    │  - Input Verify │    │ - Route Storage │
│ - SSL/TLS       │    │  - AI Analysis  │    │ - Service Disc. │
│ - CORS          │    │  - Model Loading│    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                ▲
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

**Note**: The frontend is deployed separately to Vercel for production. See `DEPLOYMENT_GUIDE.md` for details.

## Prerequisites

- Docker
- Docker Compose
- curl (for setup script)
- Git (for model downloading)

## Environment Variables

### Backend Service
- `JWT_SECRET_KEY`: Secret key for JWT token signing (required)
- `CORS_ORIGINS`: Allowed origins for CORS (default: `http://localhost:5173`)

### APISIX Service
- `ADMIN_KEY`: Admin key for APISIX management (default: `edd1c9f034335f136f87ad84b625c8f1`)

### Frontend (when deployed locally)
- `VITE_API_URL`: Base URL for API requests (default: `http://localhost:9080`)

## File Structure

```
docker/
├── docker-compose.yml          # Main Docker Compose file
├── apisix-config.yaml          # APISIX configuration
├── apisix-routes.yaml          # APISIX routes (reference)
├── setup-apisix.sh            # APISIX setup script
├── backend.Dockerfile         # Backend container definition
├── run-docker.sh              # Convenience script
└── DOCKER_README.md           # This documentation
```

## Quick Start

### Option A: Using the convenience script (Recommended)

```bash
# Make script executable
chmod +x run-docker.sh

# Start and configure everything
./run-docker.sh setup
```

### Option B: Manual commands

```bash
# Navigate to docker directory
cd docker

# Build and start all services
docker-compose up -d --build

# Wait for services to start
sleep 10

# Check service status
docker-compose ps

# Configure APISIX routes
chmod +x setup-apisix.sh
./setup-apisix.sh

# Return to project root
cd ..
```

## Access Points

- **API Gateway**: http://localhost:9080 (Main entry point)
- **APISIX Admin**: http://localhost:9180 (Admin interface)
- **Backend Direct**: http://localhost:8000 (Direct backend access)
- **Frontend**: Deployed to Vercel (see DEPLOYMENT_GUIDE.md)

## Rate Limiting Configuration

APISIX implements comprehensive rate limiting:

### Authentication Endpoints (`/auth/*`)
- **Rate**: 5 requests per 7 minutes per IP
- **Burst**: 10 requests
- **Time Window**: 420 seconds (7 minutes)
- **Purpose**: Prevent brute force authentication attacks

### Scan Endpoints (`/scan/*`)
- **Rate**: 20 requests per minute per IP
- **Burst**: 30 requests
- **Time Window**: 60 seconds
- **Timeout**: 300 seconds (5 minutes for cold start)
- **Purpose**: Prevent API abuse while allowing ML model processing

### Models Status Endpoints (`/models/*`)
- **Rate**: No limit (frequent status checks needed)
- **Timeout**: 60 seconds
- **Purpose**: Real-time model status monitoring

### History Endpoints (`/history`)
- **Rate**: 30 requests per minute per IP
- **Burst**: 50 requests
- **Time Window**: 60 seconds
- **Purpose**: Prevent dashboard spam while allowing normal usage

## Test Tokens

Use these tokens for testing:

- `sample_token_1` (User role)
- `sample_token_2` (Admin role)

## API Endpoints

All API calls should go through the APISIX gateway at `http://localhost:9080`:

- `POST /auth/token` - Authenticate with token
- `POST /scan/email` - Analyze email content
- `GET /models/status` - Check AI model status
- `GET /history` - Get analysis history
- `GET /health` - Health check

## Service Management

### Using Convenience Scripts

```bash
# Start services
./run-docker.sh up

# Stop services
./run-docker.sh down

# Restart services
./run-docker.sh restart

# View logs
./run-docker.sh logs

# Check status
./run-docker.sh status

# Clean up (remove volumes)
./run-docker.sh clean

# Build services
./run-docker.sh build

# Full setup (build + start + configure)
./run-docker.sh setup
```

### Manual Commands

```bash
# Navigate to docker directory
cd docker

# View logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f backend
docker-compose logs -f apisix
docker-compose logs -f etcd

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart specific service
docker-compose restart backend

# Return to project root
cd ..
```

## APISIX Admin API

Access APISIX admin API at `http://localhost:9180`:

```bash
# List all routes
curl -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
     http://localhost:9180/apisix/admin/routes

# Get specific route
curl -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
     http://localhost:9180/apisix/admin/routes/1

# Check services
curl -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
     http://localhost:9180/apisix/admin/services
```

## Troubleshooting

### Common Issues

1. **APISIX not starting**
   ```bash
   # Check etcd is running first
   docker-compose logs etcd
   
   # Restart APISIX
   docker-compose restart apisix
   
   # Check APISIX logs
   docker-compose logs apisix
   ```

2. **Backend models not loading**
   ```bash
   # Check backend logs for model loading status
   docker-compose logs backend | grep -E "(✓|✗|Model|Loading)"
   
   # Test models endpoint
   curl http://localhost:9080/models/status
   ```

3. **Rate limiting too strict**
   ```bash
   # Modify rate limits in setup-apisix.sh
   # Re-run the setup script
   ./setup-apisix.sh
   ```

4. **Frontend can't connect to API**
   - Ensure APISIX is running on port 9080
   - Check CORS configuration
   - Verify frontend environment variables

5. **Backend not accessible**
   ```bash
   # Check backend logs
   docker-compose logs backend
   
   # Test backend directly
   curl http://localhost:8000/health
   
   # Test through APISIX
   curl http://localhost:9080/health
   ```

6. **Git LFS model files not downloading**
   ```bash
   # Enter backend container
   docker-compose exec backend bash
   
   # Navigate to models directory
   cd /app/ai/models
   
   # Pull LFS files manually
   git lfs pull
   ```

### Debug Commands

```bash
# Check all container status
./run-docker.sh status

# Check network connectivity
docker-compose exec backend ping apisix
docker-compose exec apisix ping backend

# Test individual services
curl http://localhost:9180/apisix/admin/services \
     -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1'
curl http://localhost:8000/health
curl http://localhost:9080/health

# Check container resources
docker stats
```

### Log Analysis

```bash
# Follow all logs
docker-compose logs -f

# Filter specific patterns
docker-compose logs backend | grep -E "(ERROR|WARN|Model)"
docker-compose logs apisix | grep -E "(error|timeout|rate)"

# Check startup sequence
docker-compose logs --since=5m
```

## Security Considerations

### Production Security
- Change default admin key in `apisix-config.yaml`
- Use HTTPS/TLS certificates
- Configure proper CORS origins
- Enable authentication for APISIX admin
- Use secure JWT secret keys
- Implement proper firewall rules

### Container Security
- Images are based on official Python and Apache APISIX images
- Minimal attack surface with only necessary packages
- Non-root user execution where possible
- Health checks for service monitoring

## Performance Optimization

### Production Performance
- Use Redis for rate limiting storage instead of in-memory
- Configure proper resource limits in docker-compose.yml
- Enable APISIX caching for static responses
- Use load balancer for multiple backend instances
- Optimize AI model loading and caching

### Resource Monitoring
```bash
# Monitor container resources
docker stats

# Check disk usage
docker system df

# Clean up unused resources
docker system prune
```

## Development

### Local Development Without Docker

For development without Docker:

1. Start backend: `cd backend && python app.py`
2. Start frontend: `cd frontend && npm run dev`
3. Update frontend URLs to use `http://localhost:8000` directly

### Adding New Routes

1. Add route configuration to `setup-apisix.sh`
2. Re-run the setup script: `./setup-apisix.sh`
3. Test the new endpoint

### Modifying Configuration

1. **Rate Limits**: Update `setup-apisix.sh` and re-run
2. **APISIX Config**: Modify `apisix-config.yaml` and restart
3. **Backend Config**: Update environment variables in `docker-compose.yml`

## Monitoring and Logging

### Health Checks

All services include health checks:
- **Backend**: `/health` endpoint
- **APISIX**: Admin API connectivity
- **etcd**: Built-in health check

### Log Aggregation

```bash
# Centralized logging
docker-compose logs > app.log

# Real-time monitoring
watch -n 5 'docker-compose ps'
```

## Production Deployment

### Environment Setup
1. Set strong `JWT_SECRET_KEY`
2. Configure production CORS origins
3. Use HTTPS certificates
4. Set up monitoring and alerting
5. Configure backup strategies

### Scaling
- Use Docker Swarm or Kubernetes for orchestration
- Implement horizontal scaling for backend services
- Use external Redis for shared state
- Configure load balancing and failover

## Support and Troubleshooting

### Getting Help
- Check this documentation first
- Review container logs for errors
- Test individual components
- Verify network connectivity
- Check environment variables

### Common Solutions
- **Cold start issues**: Models take time to load initially
- **CORS errors**: Check frontend environment variables
- **Rate limiting**: Wait for time windows to reset
- **Memory issues**: Increase Docker memory limits

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test changes with Docker setup
4. Submit a pull request 
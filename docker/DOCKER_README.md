# Email Guard - Docker Setup with APISIX

This document explains how to run the Email Guard application using Docker with APISIX as the API gateway for rate limiting and routing.

## Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   APISIX        â”‚    â”‚   Backend       â”‚    â”‚   etcd          â”‚
â”‚   Gateway       â”‚â—„â”€â”€â–ºâ”‚   (FastAPI)     â”‚    â”‚   Storage       â”‚
â”‚   Port: 9080    â”‚    â”‚   Port: 8000    â”‚    â”‚   Port: 2379    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Note**: Frontend is deployed separately to Vercel. See `DEPLOYMENT_GUIDE.md` for details.

## Prerequisites

- Docker
- Docker Compose
- curl (for setup script)

## File Structure

```
email_guard_devCursor/
â”œâ”€â”€ docker/                    # Docker configuration files
â”‚   â”œâ”€â”€ docker-compose.yml     # Main Docker Compose file
â”‚   â”œâ”€â”€ apisix-config.yaml     # APISIX configuration
â”‚   â”œâ”€â”€ apisix-routes.yaml     # APISIX route definitions
â”‚   â”œâ”€â”€ setup-apisix.sh        # APISIX setup script
â”‚   â””â”€â”€ backend.Dockerfile     # Backend container definition
â”œâ”€â”€ run-docker.sh              # Convenience script (Linux/Mac)
â”œâ”€â”€ run-docker.bat             # Convenience script (Windows)
â”œâ”€â”€ backend/                   # Backend application code
â”œâ”€â”€ frontend/                  # Frontend application code
â””â”€â”€ ...
```

## Quick Start

### 1. Build and Start Services

#### Option A: Using the convenience script (Recommended)

```bash
# Start and configure everything
./run-docker.sh setup

# Or on Windows:
./run-docker.bat setup
```

#### Option B: Manual commands

```bash
# Navigate to docker directory
cd docker

# Build and start all services
docker-compose up -d --build

# Check service status
docker-compose ps

# Configure APISIX routes
chmod +x setup-apisix.sh
./setup-apisix.sh

# Return to project root
cd ..
```

### 3. Access the Application

- **API Gateway**: http://localhost:9080
- **APISIX Admin**: http://localhost:9180
- **Backend Direct**: http://localhost:8000

**Note**: Frontend is deployed to Vercel. See `DEPLOYMENT_GUIDE.md` for frontend deployment.

## Rate Limiting Configuration

APISIX handles rate limiting with the following rules:

### Authentication Endpoints (`/auth/*`)
- **Rate**: 5 requests per 7 minutes per IP
- **Burst**: 10 requests
- **Time Window**: 420 seconds (7 minutes)

### Scan Endpoints (`/scan/*`)
- **Rate**: 20 requests per minute per IP
- **Burst**: 30 requests
- **Time Window**: 60 seconds

### History Endpoints (`/history`)
- **Rate**: 30 requests per minute per IP
- **Burst**: 50 requests
- **Time Window**: 60 seconds

## Test Tokens

Use these tokens for testing:

- `sample_token_1` (User role)
- `sample_token_2` (Admin role)
- `sample_token_3` (User role)
- `sample_token_4` (User role)

## API Endpoints

All API calls should go through the APISIX gateway at `http://localhost:9080`:

- `POST /auth/token` - Authenticate with token
- `POST /scan/email` - Analyze email content
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

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart services
docker-compose restart

# Return to project root
cd ..
```

## APISIX Admin API

Access APISIX admin API at `http://localhost:9180`:

```bash
# List all routes
curl http://localhost:9180/apisix/admin/routes

# Get specific route
curl http://localhost:9180/apisix/admin/routes/1

# Update route
curl -X PUT http://localhost:9180/apisix/admin/routes/1 \
  -H 'X-API-KEY: edd1c9f034335f136f87ad84b625c8f1' \
  -H 'Content-Type: application/json' \
  -d '{...}'
```

## Troubleshooting

### Common Issues

1. **APISIX not starting**
   ```bash
   # Check etcd is running
   docker-compose logs etcd
   
   # Restart APISIX
   docker-compose restart apisix
   ```

2. **Rate limiting too strict**
   - Modify rate limits in `setup-apisix.sh`
   - Re-run the setup script

3. **Frontend can't connect to API**
   - Ensure APISIX is running on port 9080
   - Check CORS configuration

4. **Backend not accessible**
   ```bash
   # Check backend logs
   docker-compose logs backend
   
   # Test backend directly
   curl http://localhost:8000/health
   ```

### Debug Commands

```bash
# Check all container status
./run-docker.sh status

# Or manually:
cd docker
docker-compose ps
cd ..

# Check network connectivity
cd docker
docker-compose exec backend ping apisix
cd ..

# Test APISIX health
curl http://localhost:9180/apisix/admin/services

# Test backend health
curl http://localhost:8000/health
```

## Production Considerations

### Security
- Change default admin key in `apisix-config.yaml`
- Use HTTPS in production
- Configure proper CORS origins
- Enable authentication for APISIX admin

### Performance
- Use Redis for rate limiting storage
- Configure proper resource limits
- Enable APISIX caching
- Use load balancer for multiple backend instances

### Monitoring
- Enable APISIX metrics
- Configure logging aggregation
- Set up health checks
- Monitor rate limiting metrics

## Development

### Local Development

For local development without Docker:

1. Start backend: `cd backend && python app.py`
2. Start frontend: `cd frontend && npm run dev`
3. Update frontend URLs to use `http://localhost:8000` directly

### Adding New Routes

1. Add route configuration to `setup-apisix.sh`
2. Re-run the setup script
3. Test the new endpoint

### Modifying Rate Limits

1. Update rate limit configuration in `setup-apisix.sh`
2. Re-run the setup script
3. Test with appropriate load

## File Structure

```
â”œâ”€â”€ docker-compose.yml          # Main Docker Compose file
â”œâ”€â”€ apisix-config.yaml          # APISIX configuration
â”œâ”€â”€ apisix-routes.yaml          # APISIX routes (reference)
â”œâ”€â”€ setup-apisix.sh            # APISIX setup script
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ Dockerfile             # Backend container
â”‚   â””â”€â”€ ...
â”œâ”€â”€ frontend/
â”‚   â”œâ”€â”€ Dockerfile             # Frontend container
â”‚   â”œâ”€â”€ nginx.conf             # Nginx configuration
â”‚   â””â”€â”€ ...
â””â”€â”€ docs/
    â””â”€â”€ README.md              # Main documentation
``` 
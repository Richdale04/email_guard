# Email Guard - Deployment Guide

This guide explains how to deploy the Email Guard application to Vercel (frontend) and Render (backend).

## Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   Vercel        â”‚    â”‚   Render        â”‚    â”‚   Local/Cloud   â”‚
â”‚   Frontend      â”‚â—„â”€â”€â–ºâ”‚   Backend       â”‚â—„â”€â”€â–ºâ”‚   APISIX        â”‚
â”‚   (React)       â”‚    â”‚   (FastAPI)     â”‚    â”‚   (Optional)    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Frontend Deployment (Vercel)

### 1. Prepare Frontend for Vercel

The frontend is already configured for Vercel deployment with:
- `vercel.json` - Vercel configuration
- Environment variable support for API URLs
- Build configuration for Vite

### 2. Deploy to Vercel

#### Option A: Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Deploy
vercel

# Follow the prompts:
# - Link to existing project or create new
# - Set project name
# - Set environment variables
```

#### Option B: Vercel Dashboard
1. Go to [vercel.com](https://vercel.com)
2. Create new project
3. Connect your GitHub repository
4. Set root directory to `frontend`
5. Configure environment variables

### 3. Environment Variables

Set these environment variables in Vercel:

```
VITE_API_URL=https://your-backend-url.onrender.com
```

### 4. Build Settings

Vercel will automatically detect the Vite configuration:
- **Framework Preset**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

## Backend Deployment (Render)

### 1. Prepare Backend for Render

The backend is already configured for Render deployment with:
- `Dockerfile` - Container configuration
- `requirements.txt` - Python dependencies
- Health check endpoint

### 2. Deploy to Render

#### Option A: Render Dashboard
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Configure the service:

**Basic Settings:**
- **Name**: `email-guard-backend`
- **Environment**: `Docker`
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build & Deploy:**
- **Build Command**: Leave empty (uses Dockerfile)
- **Start Command**: Leave empty (uses Dockerfile CMD)

**Environment Variables:**
```
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

### 3. Environment Variables

Set these environment variables in Render:

```
# Security
SECRET_KEY=your-super-secret-key-change-this

# CORS (replace with your Vercel domain)
CORS_ORIGINS=https://your-app.vercel.app

# Optional: Database URL (if using external database)
DATABASE_URL=your-database-url

# Optional: Redis URL (if using external Redis)
REDIS_URL=your-redis-url
```

### 4. Health Check

Render will use the health check endpoint:
- **Health Check Path**: `/health`
- **Health Check Timeout**: 180 seconds

## Production Configuration

### 1. Update CORS Settings

Update the backend CORS configuration for production:

```python
# In backend/app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",  # Your Vercel domain
        "http://localhost:5173",        # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Secure JWT Configuration

Update JWT settings for production:

```python
# In backend/modules/authenticate.py
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
```

### 3. Database Configuration

For production, consider using an external database:

```python
# Add to requirements.txt
# psycopg2-binary==2.9.7  # For PostgreSQL
# pymongo==4.5.0          # For MongoDB
```

## Deployment Steps

### 1. Deploy Backend First

1. Push your code to GitHub
2. Create Render Web Service
3. Configure environment variables
4. Deploy and get the backend URL

### 2. Deploy Frontend

1. Set `VITE_API_URL` to your Render backend URL
2. Deploy to Vercel
3. Test the connection

### 3. Test the Application

1. Visit your Vercel frontend URL
2. Try authenticating with test tokens
3. Test email scanning functionality
4. Check history functionality

## Environment Variables Reference

### Frontend (Vercel)
```
VITE_API_URL=https://your-backend-url.onrender.com
```

### Backend (Render)
```
SECRET_KEY=your-super-secret-key
CORS_ORIGINS=https://your-app.vercel.app
DATABASE_URL=your-database-url (optional)
REDIS_URL=your-redis-url (optional)
```

## Monitoring and Logs

### Vercel
- **Logs**: Available in Vercel dashboard
- **Analytics**: Built-in performance monitoring
- **Functions**: Serverless function logs

### Render
- **Logs**: Available in Render dashboard
- **Metrics**: CPU, memory, and request metrics
- **Health Checks**: Automatic health monitoring

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check `CORS_ORIGINS` environment variable
   - Ensure frontend domain is included
   - Verify `allow_credentials=True`

2. **Authentication Failures**
   - Check `SECRET_KEY` is set correctly
   - Verify JWT token expiration settings
   - Check token validation logic

3. **Build Failures**
   - Check `requirements.txt` for missing dependencies
   - Verify Dockerfile configuration
   - Check build logs in Render dashboard

4. **Frontend API Connection**
   - Verify `VITE_API_URL` is correct
   - Check network connectivity
   - Test API endpoints directly

### Debug Commands

```bash
# Test backend health
curl https://your-backend-url.onrender.com/health

# Test authentication
curl -X POST https://your-backend-url.onrender.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{"token": "sample_token_1"}'

# Check CORS headers
curl -H "Origin: https://your-app.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS https://your-backend-url.onrender.com/auth/token
```

## Security Considerations

### Production Security
1. **Use strong SECRET_KEY**
2. **Enable HTTPS only**
3. **Configure proper CORS origins**
4. **Use environment variables for secrets**
5. **Enable security headers**
6. **Regular dependency updates**

### Rate Limiting
For production without APISIX, consider:
- Cloudflare rate limiting
- Render's built-in rate limiting
- Custom rate limiting middleware

## Cost Optimization

### Vercel
- Free tier: 100GB bandwidth/month
- Pro plan: $20/month for more features

### Render
- Free tier: 750 hours/month
- Starter plan: $7/month for always-on service

## Next Steps

1. **Database**: Consider adding PostgreSQL for persistent data
2. **Caching**: Add Redis for session management
3. **Monitoring**: Set up error tracking (Sentry)
4. **CDN**: Configure CDN for static assets
5. **SSL**: Ensure HTTPS is properly configured 
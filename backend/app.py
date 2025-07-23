from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime, timedelta
import json
from typing import List, Optional

from modules.authenticate import authenticate_token, create_jwt_token, verify_jwt_token
from modules.verify import verify_and_sanitize_input
from scan import scan_email, save_scan_history, get_scan_history

app = FastAPI(title="Email Guard API", version="1.0.0")



# Pydantic models
class TokenRequest(BaseModel):
    token: str

class EmailScanRequest(BaseModel):
    email_text: str

class ModelResult(BaseModel):
    model_source: str
    model_name: str
    decision: str
    confidence: float
    description: str

class ScanResponse(BaseModel):
    results: List[ModelResult]
    timestamp: str
    email_snippet: str



@app.post("/auth/token")
async def authenticate_user(request: TokenRequest, response: Response, req: Request):
    """Authenticate user with token and return JWT"""
    try:
        # Authenticate the token
        user_info = authenticate_token(request.token)
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Create JWT token
        jwt_token = create_jwt_token(user_info)
        
        # Set HTTP-only cookie
        response.set_cookie(
            key="auth_token",
            value=jwt_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=3600  # 1 hour
        )
        
        return {"message": "Authentication successful", "user": user_info}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

@app.post("/scan/email")
async def scan_email_endpoint(request: EmailScanRequest, req: Request):
    """Scan email text for phishing/spam detection"""
    try:
        # Get JWT from cookie
        auth_cookie = req.cookies.get("auth_token")
        if not auth_cookie:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        # Verify JWT
        user_info = verify_jwt_token(auth_cookie)
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        # Verify and sanitize input
        sanitized_text = verify_and_sanitize_input(request.email_text)
        
        # Scan email using AI models
        scan_results = scan_email(sanitized_text)
        
        # Check if we got any results
        if not scan_results:
            raise HTTPException(
                status_code=503, 
                detail="AI models are not ready or failed to analyze. Please try again in a moment."
            )
        
        # Save to history
        save_scan_history(user_info['sub'], sanitized_text, scan_results)
        
        # Create response
        response_data = ScanResponse(
            results=scan_results,
            timestamp=datetime.now().isoformat(),
            email_snippet=sanitized_text[:200] + "..." if len(sanitized_text) > 200 else sanitized_text
        )
        
        return response_data
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Scan error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@app.get("/history")
async def get_history(req: Request, limit: int = 10):
    """Get scan history for authenticated user"""
    try:
        # Get JWT from cookie
        auth_cookie = req.cookies.get("auth_token")
        if not auth_cookie:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        # Verify JWT
        user_info = verify_jwt_token(auth_cookie)
        if not user_info:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        # Get history
        history = get_scan_history(user_info['sub'], limit)
        
        return {"history": history}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get history: {str(e)}")

@app.post("/auth/logout")
async def logout_user(response: Response):
    """Logout user by clearing the authentication cookie"""
    response.delete_cookie(
        key="auth_token",
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax"
    )
    return {"message": "Logged out successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/models/status")
async def models_status():
    """Check if AI models are loaded and ready"""
    try:
        from scan import EMAIL_GUARD_AVAILABLE
        if EMAIL_GUARD_AVAILABLE:
            from ai.email_guard import get_model_info
            model_info = get_model_info()
            
            # Check if we have ML models loaded
            if model_info.get('ml_models_loaded', False):
                status = "ready"
            elif model_info.get('total_models', 0) > 0:
                status = "partial"  # Only rule-based models available
            else:
                status = "not_ready"
            
            return {
                "status": status,
                "models": model_info,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "not_available",
                "error": "Email guard module not available",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
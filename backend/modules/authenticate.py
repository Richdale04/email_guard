import csv
import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional, Dict, Any
import hashlib

# JWT Configuration - Add fallback for SECRET_KEY
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Token storage file path
TOKENS_FILE = "db/users.csv"

def load_tokens_from_csv() -> Dict[str, Dict[str, Any]]:
    """Load valid tokens from CSV file"""
    tokens = {}
    
    # Create users.csv if it doesn't exist
    if not os.path.exists(TOKENS_FILE):
        os.makedirs(os.path.dirname(TOKENS_FILE), exist_ok=True)
        with open(TOKENS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['token', 'sub', 'role', 'expires_at'])
            # Add some sample tokens
            writer.writerow(['sample_token_1', 'user1', 'user', '2025-12-31'])
            writer.writerow(['sample_token_2', 'user2', 'admin', '2025-12-31'])
    
    try:
        with open(TOKENS_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Strip whitespace from all values to prevent issues
                token = row['token'].strip()
                sub = row['sub'].strip()
                role = row['role'].strip()
                expires_at = row['expires_at'].strip()
                
                tokens[token] = {
                    'sub': sub,
                    'role': role,
                    'expires_at': expires_at
                }
    except FileNotFoundError:
        print(f"Warning: {TOKENS_FILE} not found. Creating with sample data.")
        # Create default tokens file
        with open(TOKENS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['token', 'sub', 'role', 'expires_at'])
            writer.writerow(['sample_token_1', 'user1', 'user', '2024-12-31'])
            writer.writerow(['sample_token_2', 'user2', 'admin', '2024-12-31'])
        
        # Load the created file
        with open(TOKENS_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Strip whitespace from all values to prevent issues
                token = row['token'].strip()
                sub = row['sub'].strip()
                role = row['role'].strip()
                expires_at = row['expires_at'].strip()
                
                tokens[token] = {
                    'sub': sub,
                    'role': role,
                    'expires_at': expires_at
                }
    
    return tokens

def authenticate_token(token: str) -> Optional[Dict[str, Any]]:
    """Authenticate user token and return user info"""
    try:
        tokens = load_tokens_from_csv()
        
        # Strip whitespace from input token to prevent issues
        token = token.strip()
        
        if token not in tokens:
            return None
        
        token_info = tokens[token]
        
        # Check if token is expired
        try:
            expires_at = datetime.strptime(token_info['expires_at'], '%Y-%m-%d')
            if datetime.now() > expires_at:
                return None
        except ValueError:
            # If date parsing fails, assume token is valid
            pass
        
        return {
            'sub': token_info['sub'],
            'role': token_info['role']
        }
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def create_jwt_token(user_info: Dict[str, Any]) -> str:
    """Create JWT token for authenticated user"""
    try:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {
            "sub": user_info['sub'],
            "role": user_info['role'],
            "exp": expire
        }
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        print(f"JWT creation error: {e}")
        raise

def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token and return user info"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        role: str = payload.get("role")
        exp: int = payload.get("exp")
        
        if sub is None or role is None or exp is None:
            return None
        
        # Check if token is expired
        if datetime.utcnow() > datetime.fromtimestamp(exp):
            return None
        
        return {"sub": sub, "role": role}
    
    except JWTError as e:
        print(f"JWT verification error: {e}")
        return None
    except Exception as e:
        print(f"JWT verification error: {e}")
        return None

def hash_token(token: str) -> str:
    """Hash token for secure storage"""
    return hashlib.sha256(token.encode()).hexdigest()

def add_token_to_csv(token: str, sub: str, role: str, expires_at: str):
    """Add a new token to the CSV file"""
    with open(TOKENS_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([token, sub, role, expires_at])
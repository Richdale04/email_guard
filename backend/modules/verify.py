import re
import html
from typing import Optional
import unicodedata

def verify_and_sanitize_input(email_text: str) -> str:
    """
    Verify and sanitize email text input
    
    Args:
        email_text: Raw email text input
        
    Returns:
        Sanitized email text
        
    Raises:
        ValueError: If input is invalid or too long
    """
    
    # Check if input is None or empty
    if not email_text or not isinstance(email_text, str):
        raise ValueError("Email text cannot be empty or null")
    
    # Remove leading/trailing whitespace
    email_text = email_text.strip()
    
    # Check length limits
    if len(email_text) == 0:
        raise ValueError("Email text cannot be empty")
    
    if len(email_text) > 10000:  # 10KB limit
        raise ValueError("Email text too long (maximum 10,000 characters)")
    
    # Normalize unicode characters
    email_text = unicodedata.normalize('NFKC', email_text)
    
    # Decode HTML entities
    email_text = html.unescape(email_text)
    
    # Remove null bytes and control characters (except newlines and tabs)
    email_text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', email_text)
    
    # Remove excessive whitespace (keep single spaces, newlines, tabs)
    email_text = re.sub(r'[ \t]+', ' ', email_text)
    email_text = re.sub(r'\n\s*\n', '\n\n', email_text)
    
    # Basic email content validation
    if not contains_email_content(email_text):
        raise ValueError("Input does not appear to contain valid email content")
    
    return email_text

def contains_email_content(text: str) -> bool:
    """
    Check if text contains basic email content indicators
    
    Args:
        text: Text to check
        
    Returns:
        True if text appears to contain email content
    """
    # Check for minimum length
    if len(text) < 10:
        return False
    
    # Check for common email indicators
    email_indicators = [
        r'@',  # Email addresses
        r'http[s]?://',  # URLs
        r'\b(?:from|to|subject|cc|bcc)\b',  # Email headers
        r'\b(?:dear|hello|hi|greetings)\b',  # Common greetings
        r'\b(?:sincerely|best|regards|thank you)\b',  # Common closings
        r'\b(?:click|login|password|account|verify)\b',  # Common email content words
    ]
    
    text_lower = text.lower()
    indicator_count = sum(1 for pattern in email_indicators if re.search(pattern, text_lower))
    
    # If at least 2 indicators are found, consider it valid email content
    return indicator_count >= 2

def extract_email_metadata(text: str) -> dict:
    """
    Extract basic metadata from email text
    
    Args:
        text: Email text
        
    Returns:
        Dictionary containing extracted metadata
    """
    metadata = {
        'word_count': len(text.split()),
        'char_count': len(text),
        'has_urls': bool(re.search(r'http[s]?://', text, re.IGNORECASE)),
        'has_email_addresses': bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
        'has_attachments': bool(re.search(r'\b(?:attachment|attached|file)\b', text, re.IGNORECASE)),
        'urgency_indicators': len(re.findall(r'\b(?:urgent|immediate|asap|emergency|critical)\b', text, re.IGNORECASE)),
        'money_indicators': len(re.findall(r'\b(?:money|bank|account|credit|debit|payment|transfer|dollar|euro|pound)\b', text, re.IGNORECASE)),
    }
    
    return metadata

def detect_suspicious_patterns(text: str) -> list:
    """
    Detect suspicious patterns in email text
    
    Args:
        text: Email text
        
    Returns:
        List of detected suspicious patterns
    """
    suspicious_patterns = []
    
    # Check for urgency
    if re.search(r'\b(?:urgent|immediate|asap|emergency|critical)\b', text, re.IGNORECASE):
        suspicious_patterns.append('urgency')
    
    # Check for financial requests
    if re.search(r'\b(?:bank|account|credit|debit|payment|transfer)\b', text, re.IGNORECASE):
        suspicious_patterns.append('financial_request')
    
    # Check for personal information requests
    if re.search(r'\b(?:password|ssn|social security|credit card|account number)\b', text, re.IGNORECASE):
        suspicious_patterns.append('personal_info_request')
    
    # Check for suspicious URLs
    if re.search(r'http[s]?://[^\s]*\.(?:tk|ml|ga|cf|gq)', text, re.IGNORECASE):
        suspicious_patterns.append('suspicious_domain')
    
    # Check for excessive punctuation
    if text.count('!') > 3 or text.count('?') > 3:
        suspicious_patterns.append('excessive_punctuation')
    
    # Check for all caps
    if len(re.findall(r'\b[A-Z]{3,}\b', text)) > 5:
        suspicious_patterns.append('excessive_caps')
    
    return suspicious_patterns
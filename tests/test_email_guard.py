import pytest
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from modules.verify import verify_and_sanitize_input, contains_email_content
from modules.authenticate import authenticate_token, create_jwt_token, verify_jwt_token

class TestEmailVerification:
    """Test email verification and sanitization"""
    
    def test_valid_email_content(self):
        """Test that valid email content passes verification"""
        email_text = """
        Dear John,
        
        Please review the attached documents for the project.
        Let me know if you have any questions.
        
        Best regards,
        Sarah
        """
        
        result = verify_and_sanitize_input(email_text)
        assert result is not None
        assert len(result) > 0
    
    def test_empty_email(self):
        """Test that empty email raises ValueError"""
        with pytest.raises(ValueError, match="Email text cannot be empty"):
            verify_and_sanitize_input("")
    
    def test_none_email(self):
        """Test that None email raises ValueError"""
        with pytest.raises(ValueError, match="Email text cannot be empty or null"):
            verify_and_sanitize_input(None)
    
    def test_too_long_email(self):
        """Test that very long email raises ValueError"""
        long_email = "A" * 10001
        with pytest.raises(ValueError, match="Email text too long"):
            verify_and_sanitize_input(long_email)
    
    def test_contains_email_content(self):
        """Test email content detection"""
        # Valid email content
        valid_content = "Dear user, please click here to verify your account."
        assert contains_email_content(valid_content) == True
        
        # Invalid content (too short)
        invalid_content = "Hi"
        assert contains_email_content(invalid_content) == False

class TestAuthentication:
    """Test authentication functionality"""
    
    def test_authenticate_valid_token(self):
        """Test authentication with valid token"""
        # This test requires the tokens.csv file to exist
        # In a real test environment, you'd mock the file or create test data
        pass
    
    def test_create_jwt_token(self):
        """Test JWT token creation"""
        user_info = {
            'sub': 'test_user',
            'role': 'user'
        }
        
        token = create_jwt_token(user_info)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_jwt_token(self):
        """Test JWT token verification"""
        user_info = {
            'sub': 'test_user',
            'role': 'user'
        }
        
        # Create token
        token = create_jwt_token(user_info)
        
        # Verify token
        verified_info = verify_jwt_token(token)
        assert verified_info is not None
        assert verified_info['sub'] == user_info['sub']
        assert verified_info['role'] == user_info['role']
    
    def test_verify_invalid_token(self):
        """Test verification of invalid token"""
        invalid_token = "invalid.jwt.token"
        result = verify_jwt_token(invalid_token)
        assert result is None

class TestEmailAnalysis:
    """Test email analysis functionality"""
    
    def test_phishing_detection(self):
        """Test phishing email detection"""
        phishing_email = """
        Dear Customer,
        
        Your account has been suspended due to suspicious activity.
        Please click here immediately to verify your identity:
        http://fake-bank.tk/verify
        
        This is URGENT!
        """
        
        # Test that phishing indicators are detected
        from modules.verify import detect_suspicious_patterns
        patterns = detect_suspicious_patterns(phishing_email)
        
        assert 'urgency' in patterns or 'financial_request' in patterns
    
    def test_spam_detection(self):
        """Test spam email detection"""
        spam_email = """
        CONGRATULATIONS! You've won a FREE prize!
        Click here to claim your reward:
        http://amazing-offers.ga/prize
        
        Limited time offer!
        """
        
        from modules.verify import detect_suspicious_patterns
        patterns = detect_suspicious_patterns(spam_email)
        
        # Should detect spam patterns
        assert len(patterns) > 0
    
    def test_safe_email(self):
        """Test safe email detection"""
        safe_email = """
        Hi John,
        
        Thanks for your email. I've reviewed the documents and everything looks good.
        Let's schedule a meeting next week.
        
        Best regards,
        Sarah
        """
        
        from modules.verify import detect_suspicious_patterns
        patterns = detect_suspicious_patterns(safe_email)
        
        # Should have few or no suspicious patterns
        assert len(patterns) == 0 or len(patterns) <= 1

if __name__ == "__main__":
    pytest.main([__file__])

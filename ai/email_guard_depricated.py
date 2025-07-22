# ai/email_guard.py
import os
import sys
from typing import List, Dict, Any, Optional, Callable
import re
import numpy as np
from datetime import datetime

# Add models directory to path
# Get the actual directory of this file, not the importing file
models_dir = '/app/ai/models/'

# Try to import ML libraries
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Warning: ML libraries not available. Using rule-based analysis only.")

# Try to import phishing-detector
try:
    from phishing_detector import PhishingDetector
    PHISHING_DETECTOR_AVAILABLE = True
except ImportError:
    PHISHING_DETECTOR_AVAILABLE = False
    print("Warning: phishing-detector not available.")

class ModelAnalyzer:
    """Base class for all model analyzers"""
    
    def __init__(self, model_name: str, model_source: str):
        self.model_name = model_name
        self.model_source = model_source
    
    def analyze(self, email_text: str) -> Dict[str, Any]:
        """Analyze email text and return results"""
        raise NotImplementedError("Subclasses must implement analyze method")

class CybersectonyDistilbertAnalyzer(ModelAnalyzer):
    """Analyzer for cybersectony-phishing-email-detection-distilbert_v2.1 model"""
    
    def __init__(self):
        super().__init__("cybersectony-distilbert", "HuggingFace")
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_model()
    
    def load_model(self):
        """Load the model and tokenizer"""
        if not ML_AVAILABLE:
            return
        
        model_path = os.path.join(models_dir, "cybersectony-phishing-email-detection-distilbert_v2.1")
        if os.path.exists(model_path):
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
                self.model.to(self.device)
                self.model.eval()
                print(f"Loaded model: {self.model_name}")
            except Exception as e:
                print(f"Failed to load model {self.model_name}: {e}")
    
    def analyze(self, email_text: str) -> Dict[str, Any]:
        """Analyze email using cybersectony model"""
        if not self.model or not self.tokenizer:
            return self._error_result("Model not loaded")
        
        try:
            # Preprocess and tokenize
            inputs = self.tokenizer(
                email_text,
                return_tensors="pt",
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get probabilities for each class
            probs = predictions[0].tolist()
            
            # Create labels dictionary
            labels = {
                "legitimate_email": probs[0],
                "phishing_url": probs[1],
                "legitimate_url": probs[2],
                "phishing_url_alt": probs[3]
            }
            
            # Determine the most likely classification
            max_label = max(labels.items(), key=lambda x: x[1])
            
            # Map to standard decision format
            if "phishing" in max_label[0]:
                decision = "phishing"
            elif "legitimate" in max_label[0]:
                decision = "safe"
            else:
                decision = "unknown"
            
            return {
                "model_source": self.model_source,
                "model_name": self.model_name,
                "decision": decision,
                "confidence": max_label[1],
                "description": f"Prediction: {max_label[0]} with {max_label[1]:.2%} confidence"
            }
            
        except Exception as e:
            return self._error_result(f"Analysis failed: {str(e)}")
    
    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        return {
            "model_source": self.model_source,
            "model_name": self.model_name,
            "decision": "error",
            "confidence": 0.0,
            "description": error_msg
        }

class AamoshDistilbertAnalyzer(ModelAnalyzer):
    """Analyzer for aamoshdahal-email-phishing-distilbert-finetuned model"""
    
    def __init__(self):
        super().__init__("aamosh-distilbert", "HuggingFace")
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_model()
    
    def load_model(self):
        """Load the model and tokenizer"""
        if not ML_AVAILABLE:
            return
        
        model_path = os.path.join(models_dir, "aamoshdahal-email-phishing-distilbert-finetuned")
        if os.path.exists(model_path):
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
                self.model.to(self.device)
                self.model.eval()
                print(f"Loaded model: {self.model_name}")
            except Exception as e:
                print(f"Failed to load model {self.model_name}: {e}")
    
    def analyze(self, email_text: str) -> Dict[str, Any]:
        """Analyze email using aamosh model"""
        if not self.model or not self.tokenizer:
            return self._error_result("Model not loaded")
        
        try:
            # Tokenize and prepare the input
            encoded_input = self.tokenizer(
                email_text, 
                return_tensors='pt', 
                truncation=True, 
                padding=True
            ).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(**encoded_input)
                probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            
            # Output prediction
            labels = ["legitimate", "phishing"]
            pred_label = labels[probs.argmax()]
            confidence = probs.max().item()
            
            # Map to standard decision format
            if pred_label == "phishing":
                decision = "phishing"
            elif pred_label == "legitimate":
                decision = "safe"
            else:
                decision = "unknown"
            
            return {
                "model_source": self.model_source,
                "model_name": self.model_name,
                "decision": decision,
                "confidence": confidence,
                "description": f"Prediction: {pred_label} with {confidence:.2%} confidence"
            }
            
        except Exception as e:
            return self._error_result(f"Analysis failed: {str(e)}")
    
    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        return {
            "model_source": self.model_source,
            "model_name": self.model_name,
            "decision": "error",
            "confidence": 0.0,
            "description": error_msg
        }

class PhishingDetectorAnalyzer(ModelAnalyzer):
    """Analyzer using the phishing-detector package"""
    
    def __init__(self):
        super().__init__("phishing-detector", "PyPI")
        self.detector = None
        self.load_model()
    
    def load_model(self):
        """Load the phishing detector"""
        if not PHISHING_DETECTOR_AVAILABLE:
            return
        
        try:
            self.detector = PhishingDetector()
            print(f"Loaded model: {self.model_name}")
        except Exception as e:
            print(f"Failed to load model {self.model_name}: {e}")
    
    def analyze(self, email_text: str) -> Dict[str, Any]:
        """Analyze email using phishing-detector"""
        if not self.detector:
            return self._error_result("Model not loaded")
        
        try:
            # Use the phishing detector
            result = self.detector.predict(email_text)
            
            # Map result to standard format
            if hasattr(result, 'prediction'):
                prediction = result.prediction
                confidence = getattr(result, 'confidence', 0.8)
            else:
                # Handle different result formats
                prediction = str(result).lower()
                confidence = 0.8
            
            # Map to standard decision format
            if "phishing" in prediction or "malicious" in prediction:
                decision = "phishing"
            elif "safe" in prediction or "legitimate" in prediction:
                decision = "safe"
            else:
                decision = "unknown"
            
            return {
                "model_source": self.model_source,
                "model_name": self.model_name,
                "decision": decision,
                "confidence": confidence,
                "description": f"Phishing detector prediction: {prediction}"
            }
            
        except Exception as e:
            return self._error_result(f"Analysis failed: {str(e)}")
    
    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        return {
            "model_source": self.model_source,
            "model_name": self.model_name,
            "decision": "error",
            "confidence": 0.0,
            "description": error_msg
        }

class RuleBasedAnalyzer(ModelAnalyzer):
    """Rule-based analyzer as fallback"""
    
    def __init__(self):
        super().__init__("rule-based", "Pattern Matching")
    
    def analyze(self, email_text: str) -> Dict[str, Any]:
        """Perform rule-based analysis"""
        text_lower = email_text.lower()
        
        # Define patterns for different types of threats
        phishing_patterns = [
            r'\b(?:urgent|immediate|asap|emergency|critical)\b',
            r'\b(?:bank|account|credit|debit|payment|transfer)\b',
            r'\b(?:password|ssn|social security|credit card)\b',
            r'\b(?:click here|login|verify|confirm)\b',
            r'http[s]?://[^\s]*\.(?:tk|ml|ga|cf|gq)',
            r'\b(?:microsoft|google|apple|amazon|paypal)\b.*\b(?:suspended|locked|verify)\b'
        ]
        
        spam_patterns = [
            r'\b(?:free|discount|offer|limited time|act now)\b',
            r'\b(?:lottery|winner|prize|claim)\b',
            r'\b(?:viagra|cialis|weight loss|diet)\b',
            r'\b(?:investment|bitcoin|crypto|money making)\b'
        ]
        
        # Count matches
        phishing_score = sum(len(re.findall(pattern, text_lower)) for pattern in phishing_patterns)
        spam_score = sum(len(re.findall(pattern, text_lower)) for pattern in spam_patterns)
        
        # Calculate risk scores
        total_score = phishing_score * 2 + spam_score
        
        if total_score >= 6:
            decision = 'phishing'
            confidence = min(0.9, 0.6 + (total_score - 6) * 0.1)
        elif total_score >= 3:
            decision = 'spam'
            confidence = min(0.8, 0.5 + (total_score - 3) * 0.1)
        else:
            decision = 'safe'
            confidence = max(0.6, 1.0 - total_score * 0.1)
        
        return {
            'model_source': self.model_source,
            'model_name': self.model_name,
            'decision': decision,
            'confidence': confidence,
            'description': f'Pattern analysis: {phishing_score} phishing indicators, {spam_score} spam indicators'
        }

class EmailAnalyzer:
    """Main email analysis class that coordinates multiple models"""
    
    def __init__(self):
        self.analyzers: List[ModelAnalyzer] = []
        self.load_analyzers()
    
    def load_analyzers(self):
        """Load all available analyzers"""
        # Add ML model analyzers
        if ML_AVAILABLE:
            self.analyzers.append(CybersectonyDistilbertAnalyzer())
            self.analyzers.append(AamoshDistilbertAnalyzer())
        
        # Add phishing-detector analyzer
        if PHISHING_DETECTOR_AVAILABLE:
            self.analyzers.append(PhishingDetectorAnalyzer())
        
        # Always add rule-based analyzer as fallback
        self.analyzers.append(RuleBasedAnalyzer())
        
        print(f"Loaded {len(self.analyzers)} analyzers")
    
    def add_analyzer(self, analyzer: ModelAnalyzer):
        """Add a custom analyzer"""
        self.analyzers.append(analyzer)
        print(f"Added custom analyzer: {analyzer.model_name}")
    
    def analyze_email(self, email_text: str) -> List[Dict[str, Any]]:
        """Analyze email text with all available models"""
        results = []
        
        for analyzer in self.analyzers:
            try:
                result = analyzer.analyze(email_text)
                results.append(result)
            except Exception as e:
                # Add error result for failed analyzer
                results.append({
                    'model_source': analyzer.model_source,
                    'model_name': analyzer.model_name,
                    'decision': 'error',
                    'confidence': 0.0,
                    'description': f'Analyzer failed: {str(e)}'
                })
        
        return results

# Global analyzer instance
_analyzer = None

def get_analyzer() -> EmailAnalyzer:
    """Get or create global analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = EmailAnalyzer()
    return _analyzer

def analyze_email_with_models(email_text: str) -> List[Dict[str, Any]]:
    """
    Main function to analyze email text with multiple models
    
    Args:
        email_text: Email text to analyze
        
    Returns:
        List of analysis results from different models
    """
    try:
        analyzer = get_analyzer()
        results = analyzer.analyze_email(email_text)
        return results
    except Exception as e:
        # Return error result if analysis fails
        return [{
            'model_source': 'system',
            'model_name': 'error_handler',
            'decision': 'error',
            'confidence': 0.0,
            'description': f'Analysis failed: {str(e)}'
        }]

def get_model_info() -> Dict[str, Any]:
    """Get information about available models"""
    analyzer = get_analyzer()
    return {
        'total_analyzers': len(analyzer.analyzers),
        'analyzers': [a.model_name for a in analyzer.analyzers],
        'ml_available': ML_AVAILABLE,
        'phishing_detector_available': PHISHING_DETECTOR_AVAILABLE
    }

def add_custom_analyzer(analyzer: ModelAnalyzer):
    """Add a custom analyzer to the global instance"""
    analyzer_instance = get_analyzer()
    analyzer_instance.add_analyzer(analyzer)

# Test function
if __name__ == "__main__":
    # Test with sample email
    test_email = """
    Dear Customer,
    
    Your account has been suspended due to suspicious activity. 
    Please click here to verify your identity: http://fake-bank.tk/verify
    
    This is urgent and requires immediate attention.
    
    Best regards,
    Bank Security Team
    """
    
    results = analyze_email_with_models(test_email)
    print("Analysis Results:")
    for result in results:
        print(f"- {result['model_name']}: {result['decision']} ({result['confidence']:.2%})")
        print(f"  {result['description']}")
        print()
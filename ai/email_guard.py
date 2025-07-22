# ai/email_guard.py
import os
import sys
from typing import List, Dict, Any, Optional
import re
from datetime import datetime

# Add models directory to path
models_dir = 'app/ai/models/'

# Try to import ML libraries
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Warning: ML libraries not available.")

# Try to import phishing_detection_py
try:
    from phishing_detection_py import PhishingDetector
    PHISHING_DETECTOR_AVAILABLE = True
except ImportError:
    PHISHING_DETECTOR_AVAILABLE = False
    print("Warning: phishing_detection_py not available.")

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
        print(f"Checking model path: {model_path}")
        print(f"Model path exists: {os.path.exists(model_path)}")
        
        if os.path.exists(model_path):
            # Check if required files exist
            required_files = ['config.json', 'pytorch_model.bin', 'tokenizer.json']
            missing_files = []
            for file in required_files:
                file_path = os.path.join(model_path, file)
                if not os.path.exists(file_path):
                    missing_files.append(file)
            
            if missing_files:
                print(f"✗ Missing files in {self.model_name}: {missing_files}")
                return
            
            try:
                print(f"Loading tokenizer from: {model_path}")
                self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
                print(f"Loading model from: {model_path}")
                self.model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
                self.model.to(self.device)
                self.model.eval()
                print(f"✓ Loaded model: {self.model_name}")
            except Exception as e:
                print(f"✗ Failed to load model {self.model_name}: {e}")
        else:
            print(f"✗ Model path does not exist: {model_path}")
    
    def analyze(self, email_text: str) -> Dict[str, Any]:
        """Analyze email using cybersectony model"""
        if not self.model or not self.tokenizer:
            return None
        
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
            print(f"Cybersectony model error: {e}")
            return None

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
        print(f"Checking model path: {model_path}")
        print(f"Model path exists: {os.path.exists(model_path)}")
        
        if os.path.exists(model_path):
            # Check if required files exist
            required_files = ['config.json', 'pytorch_model.bin', 'tokenizer.json']
            missing_files = []
            for file in required_files:
                file_path = os.path.join(model_path, file)
                if not os.path.exists(file_path):
                    missing_files.append(file)
            
            if missing_files:
                print(f"✗ Missing files in {self.model_name}: {missing_files}")
                return
            
            try:
                print(f"Loading tokenizer from: {model_path}")
                self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
                print(f"Loading model from: {model_path}")
                self.model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
                self.model.to(self.device)
                self.model.eval()
                print(f"✓ Loaded model: {self.model_name}")
            except Exception as e:
                print(f"✗ Failed to load model {self.model_name}: {e}")
        else:
            print(f"✗ Model path does not exist: {model_path}")
    
    def analyze(self, email_text: str) -> Dict[str, Any]:
        """Analyze email using aamosh model"""
        if not self.model or not self.tokenizer:
            return None
        
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
            print(f"Aamosh model error: {e}")
            return None

class PhishingDetectorAnalyzer(ModelAnalyzer):
    """Primary analyzer using phishing-detection-py package"""
    
    def __init__(self):
        super().__init__("phishing-detection-py", "PyPI")
        self.detector = None
        self.load_model()
    
    def load_model(self):
        """Load the phishing detector model"""
        if not PHISHING_DETECTOR_AVAILABLE:
            print("Warning: phishing-detection-py not available")
            return
        
        try:
            # Initialize the phishing detector for URL analysis
            self.detector = PhishingDetector(model_type="url")
            print(f"Loaded primary model: {self.model_name}")
        except Exception as e:
            print(f"Failed to load primary model {self.model_name}: {e}")
    
    def analyze(self, email_text: str) -> Dict[str, Any]:
        """Analyze email using phishing-detection-py"""
        # Only analyze if detector is available
        if not self.detector:
            return None
        
        try:
            # Extract URLs from email text for analysis
            urls = self._extract_urls(email_text)
            
            # Only analyze if URLs are present
            if not urls:
                return None
            
            # Analyze the first URL using the detector
            url_result = self.detector.predict(urls[0])
            
            # Process the result - phishing-detection-py returns a dict with prediction and description
            if url_result is not None:
                if isinstance(url_result, dict):
                    # Extract prediction and description from the result
                    prediction = url_result.get('prediction', 0)
                    description = url_result.get('description', 'No description available')
                    confidence = url_result.get('confidence', 0.85)
                else:
                    # Handle if result is just a prediction value
                    prediction = url_result
                    description = f'URL analysis result for {urls[0]}'
                    confidence = 0.85
                
                # Map prediction to standard format
                if prediction == 1:
                    decision = 'phishing'
                elif prediction == 0:
                    decision = 'safe'
                else:
                    decision = 'unknown'
                
                return {
                    'model_source': self.model_source,
                    'model_name': self.model_name,
                    'decision': decision,
                    'confidence': confidence,
                    'description': description
                }
            
            return None
            
        except Exception as e:
            print(f"Phishing detector analysis error: {e}")
            return None
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from email text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        return urls

class RuleBasedAnalyzer(ModelAnalyzer):
    """Rule-based analyzer for pattern matching and content analysis"""
    
    def __init__(self):
        super().__init__("rule-based", "built-in")
    
    def analyze(self, email_text: str) -> Dict[str, Any]:
        """Analyze email using rule-based approach"""
        try:
            # Extract metadata
            metadata = self._extract_metadata(email_text.lower())
            suspicious_patterns = self._detect_suspicious_patterns(email_text)
            
            # Calculate risk score
            risk_score = 0
            risk_factors = []
            
            # Check for suspicious patterns
            if 'urgency' in suspicious_patterns:
                risk_score += 30
                risk_factors.append('Urgency indicators detected')
            
            if 'financial_request' in suspicious_patterns:
                risk_score += 40
                risk_factors.append('Financial request detected')
            
            if 'personal_info_request' in suspicious_patterns:
                risk_score += 50
                risk_factors.append('Personal information request detected')
            
            if 'suspicious_domain' in suspicious_patterns:
                risk_score += 60
                risk_factors.append('Suspicious domain detected')
            
            # Check metadata
            if metadata['urgency_indicators'] > 0:
                risk_score += metadata['urgency_indicators'] * 10
                risk_factors.append(f'{metadata["urgency_indicators"]} urgency indicators')
            
            if metadata['money_indicators'] > 0:
                risk_score += metadata['money_indicators'] * 15
                risk_factors.append(f'{metadata["money_indicators"]} financial indicators')
            
            # Determine decision based on risk score
            if risk_score >= 70:
                decision = 'phishing'
                confidence = min(risk_score / 100.0, 0.95)
            elif risk_score >= 40:
                decision = 'spam'
                confidence = min(risk_score / 70.0, 0.85)
            else:
                decision = 'safe'
                confidence = max(1.0 - (risk_score / 40.0), 0.6)
            
            # Create detailed description
            if risk_factors:
                description = f'Risk score: {risk_score}/100. Detected factors: {", ".join(risk_factors)}. This analysis is based on pattern matching and content analysis.'
            else:
                description = f'Risk score: {risk_score}/100. No suspicious patterns detected. Email appears to be safe based on rule-based analysis.'
            
            return {
                'model_source': self.model_source,
                'model_name': self.model_name,
                'decision': decision,
                'confidence': confidence,
                'description': description
            }
            
        except Exception as e:
            return None
    
    def _extract_metadata(self, text: str) -> Dict[str, Any]:
        """Extract metadata from email text"""
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        
        # Count urgency indicators
        urgency_words = ['urgent', 'immediate', 'asap', 'quickly', 'hurry', 'limited time', 'expires', 'deadline']
        urgency_indicators = sum(1 for word in urgency_words if word in text)
        
        # Count money indicators
        money_words = ['money', 'bank', 'account', 'credit card', 'payment', 'transfer', 'refund', 'lottery', 'inheritance']
        money_indicators = sum(1 for word in money_words if word in text)
        
        # Check for URLs and email addresses
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        has_urls = bool(re.search(url_pattern, text))
        has_email_addresses = bool(re.search(email_pattern, text))
        
        return {
            'word_count': word_count,
            'char_count': char_count,
            'urgency_indicators': urgency_indicators,
            'money_indicators': money_indicators,
            'has_urls': has_urls,
            'has_email_addresses': has_email_addresses
        }
    
    def _detect_suspicious_patterns(self, text: str) -> List[str]:
        """Detect suspicious patterns in email text"""
        patterns = []
        
        # Urgency patterns
        urgency_patterns = [
            r'urgent.*action',
            r'limited.*time',
            r'expires.*soon',
            r'act.*now',
            r'immediate.*attention'
        ]
        
        for pattern in urgency_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                patterns.append('urgency')
                break
        
        # Financial request patterns
        financial_patterns = [
            r'bank.*account',
            r'credit.*card',
            r'payment.*required',
            r'money.*transfer',
            r'account.*verification'
        ]
        
        for pattern in financial_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                patterns.append('financial_request')
                break
        
        # Personal info request patterns
        personal_patterns = [
            r'social.*security',
            r'password.*reset',
            r'personal.*information',
            r'verify.*identity',
            r'account.*details'
        ]
        
        for pattern in personal_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                patterns.append('personal_info_request')
                break
        
        # Suspicious domain patterns
        suspicious_domains = [
            r'paypal.*verify',
            r'bank.*secure',
            r'account.*update',
            r'security.*alert'
        ]
        
        for pattern in suspicious_domains:
            if re.search(pattern, text, re.IGNORECASE):
                patterns.append('suspicious_domain')
                break
        
        return patterns

class EmailAnalyzer:
    """Main email analyzer that coordinates multiple models"""
    
    def __init__(self):
        self.analyzers = []
        self.load_analyzers()
    
    def load_analyzers(self):
        """Load available analyzers"""
        print(f"ML_AVAILABLE: {ML_AVAILABLE}")
        print(f"PHISHING_DETECTOR_AVAILABLE: {PHISHING_DETECTOR_AVAILABLE}")
        
        # Load HuggingFace models
        if ML_AVAILABLE:
            try:
                cybersectony_analyzer = CybersectonyDistilbertAnalyzer()
                if cybersectony_analyzer.model:  # Only add if successfully loaded
                    self.add_analyzer(cybersectony_analyzer)
                    print("✓ Cybersectony model loaded")
                else:
                    print("✗ Cybersectony model failed to load")
            except Exception as e:
                print(f"Failed to load Cybersectony model: {e}")
            
            try:
                aamosh_analyzer = AamoshDistilbertAnalyzer()
                if aamosh_analyzer.model:  # Only add if successfully loaded
                    self.add_analyzer(aamosh_analyzer)
                    print("✓ Aamosh model loaded")
                else:
                    print("✗ Aamosh model failed to load")
            except Exception as e:
                print(f"Failed to load Aamosh model: {e}")
        
        # Try to load phishing-detection-py as primary analyzer
        if PHISHING_DETECTOR_AVAILABLE:
            try:
                phishing_analyzer = PhishingDetectorAnalyzer()
                if phishing_analyzer.detector:  # Only add if successfully loaded
                    self.add_analyzer(phishing_analyzer)
                    print("✓ Primary ML analyzer loaded")
                else:
                    print("✗ Primary ML analyzer failed to load detector")
            except Exception as e:
                print(f"Failed to load primary ML analyzer: {e}")
        else:
            print("✗ phishing-detection-py package not available")
        
        # Always add rule-based analyzer
        self.add_analyzer(RuleBasedAnalyzer())
        print("✓ Rule-based analyzer loaded")
        
        print(f"Total analyzers loaded: {len(self.analyzers)}")

    def add_analyzer(self, analyzer: ModelAnalyzer):
        """Add an analyzer to the list"""
        self.analyzers.append(analyzer)
    
    def analyze_email(self, email_text: str) -> List[Dict[str, Any]]:
        """Analyze email using all available models"""
        results = []
        
        for analyzer in self.analyzers:
            try:
                result = analyzer.analyze(email_text)
                # Only add result if analysis was successful (not None)
                if result is not None:
                    results.append(result)
            except Exception as e:
                # Skip failed analyzers instead of adding error results
                print(f"Analyzer {analyzer.model_name} failed: {e}")
                continue
        
        return results

# Global analyzer instance
_analyzer = None

def get_analyzer() -> EmailAnalyzer:
    """Get or create the global analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = EmailAnalyzer()
    return _analyzer

def analyze_email_with_models(email_text: str) -> List[Dict[str, Any]]:
    """
    Main function to analyze email with all available models
    
    Args:
        email_text: Email text to analyze
        
    Returns:
        List of model results with required fields (only successful analyses)
    """
    analyzer = get_analyzer()
    return analyzer.analyze_email(email_text)

def get_model_info() -> Dict[str, Any]:
    """Get information about available models"""
    analyzer = get_analyzer()
    models = []
    
    for analyzer_instance in analyzer.analyzers:
        models.append({
            'name': analyzer_instance.model_name,
            'source': analyzer_instance.model_source,
            'status': 'loaded' if hasattr(analyzer_instance, 'detector') and analyzer_instance.detector else 'available'
        })
    
    return {
        'total_models': len(models),
        'models': models,
        'primary_ml_available': PHISHING_DETECTOR_AVAILABLE,
        'primary_model': 'phishing-detection-py' if PHISHING_DETECTOR_AVAILABLE else 'rule-based'
    }

def add_custom_analyzer(analyzer: ModelAnalyzer):
    """Add a custom analyzer to the global analyzer"""
    global_analyzer = get_analyzer()
    global_analyzer.add_analyzer(analyzer)
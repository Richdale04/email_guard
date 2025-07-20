# Email Guard AI - Modular Analysis System

## Overview

The Email Guard system provides a modular and scalable architecture for email threat detection using multiple AI models and rule-based analysis.

## Architecture

### Core Components

1. **ModelAnalyzer** - Base class for all analyzers
2. **EmailAnalyzer** - Main orchestrator that manages multiple analyzers
3. **Individual Model Analyzers** - Specific implementations for each model

### Available Analyzers

1. **CybersectonyDistilbertAnalyzer** - Uses cybersectony-phishing-email-detection-distilbert_v2.1
2. **AamoshDistilbertAnalyzer** - Uses aamoshdahal-email-phishing-distilbert-finetuned
3. **PhishingDetectorAnalyzer** - Uses the phishing-detector PyPI package
4. **RuleBasedAnalyzer** - Pattern-based fallback analysis

## Usage

### Basic Usage

```python
from ai.email_guard import analyze_email_with_models

# Analyze an email
email_text = "Your account has been suspended..."
results = analyze_email_with_models(email_text)

# Print results
for result in results:
    print(f"{result['model_name']}: {result['decision']} ({result['confidence']:.2%})")
```

### Adding Custom Analyzers

To add a new model, create a custom analyzer class:

```python
from ai.email_guard import ModelAnalyzer, add_custom_analyzer

class MyCustomAnalyzer(ModelAnalyzer):
    def __init__(self):
        super().__init__("my-custom-model", "Custom")
        # Initialize your model here
    
    def analyze(self, email_text: str) -> Dict[str, Any]:
        # Implement your analysis logic
        return {
            "model_source": self.model_source,
            "model_name": self.model_name,
            "decision": "phishing",  # or "safe", "spam", "unknown"
            "confidence": 0.85,
            "description": "Custom analysis result"
        }

# Add to the global analyzer
add_custom_analyzer(MyCustomAnalyzer())
```

### Model Requirements

Each model should be placed in the `ai/models/` directory:

```
ai/models/
├── cybersectony-phishing-email-detection-distilbert_v2.1/
│   ├── config.json
│   ├── model.safetensors
│   └── vocab.txt
└── aamoshdahal-email-phishing-distilbert-finetuned/
    ├── config.json
    ├── model.safetensors
    └── vocab.txt
```

## Output Format

All analyzers return results in a standardized format:

```python
{
    "model_source": "HuggingFace|PyPI|Custom|Pattern Matching",
    "model_name": "model-identifier",
    "decision": "phishing|safe|spam|unknown|error",
    "confidence": 0.0-1.0,
    "description": "Human-readable explanation"
}
```

## Error Handling

The system gracefully handles:
- Missing model files
- Import errors for optional dependencies
- Analysis failures
- Model loading errors

## Dependencies

### Required
- transformers
- torch
- numpy

### Optional
- phishing-detector (for PhishingDetectorAnalyzer)

## Testing

Run the built-in test:

```bash
cd ai
python email_guard.py
```

This will test all available analyzers with a sample phishing email. 
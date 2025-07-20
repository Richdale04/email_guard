#!/bin/bash

echo "🚀 Starting Email Guard Backend..."

# Check for AI models
echo "📥 Checking for AI models..."
if [ -d "/app/ai/models/cybersectony-phishing-email-detection-distilbert_v2.1" ] && [ -d "/app/ai/models/aamoshdahal-email-phishing-distilbert-finetuned" ]; then
    echo "✅ Models already exist in /app/ai/models/"
    ls -la /app/ai/models/
else
    echo "📥 Downloading missing models..."
    cd /app/ai
    git lfs install
    
    if [ ! -d "/app/ai/models/cybersectony-phishing-email-detection-distilbert_v2.1" ]; then
        echo "   Downloading cybersectony model..."
        git clone https://huggingface.co/cybersectony/phishing-email-detection-distilbert_v2.1 models/cybersectony-phishing-email-detection-distilbert_v2.1
    fi
    
    if [ ! -d "/app/ai/models/aamoshdahal-email-phishing-distilbert-finetuned" ]; then
        echo "   Downloading aamosh model..."
        git clone https://huggingface.co/aamoshdahal/email-phishing-distilbert-finetuned models/aamoshdahal-email-phishing-distilbert-finetuned
    fi
fi

echo "✅ Models ready!"

# Start the application
echo "🚀 Starting FastAPI server..."
exec uvicorn app:app --host 0.0.0.0 --port 8000
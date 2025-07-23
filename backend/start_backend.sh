#!/bin/bash

echo "Starting Email Guard Backend..."

# Check for AI models
echo "Checking for AI models..."
if [ -d "/app/ai/models/cybersectony-phishing-email-detection-distilbert_v2.1" ] && [ -d "/app/ai/models/aamoshdahal-email-phishing-distilbert-finetuned" ]; then
    echo "   Models already exist in /app/ai/models/"
    ls -la /app/ai/models/
else
    echo "Downloading missing models..."
    cd /app/ai
    git lfs install
    
    if [ ! -d "/app/ai/models/cybersectony-phishing-email-detection-distilbert_v2.1" ]; then
        echo "   Downloading cybersectony model..."
        git clone https://huggingface.co/cybersectony/phishing-email-detection-distilbert_v2.1 models/cybersectony-phishing-email-detection-distilbert_v2.1
    fi
    
    if [ ! -d "/app/ai/models/aamoshdahal-email-phishing-distilbert-finetuned" ]; then
        echo "   Downloading aamoshdahal model..."
        git clone https://huggingface.co/aamoshdahal/email-phishing-distilbert-finetuned models/aamoshdahal-email-phishing-distilbert-finetuned
    fi
fi

echo "Models ready!"

# Start model preloading in background (non-blocking)
echo "Starting model preloading in background..."
cd /app
python3 -c "
import sys
sys.path.append('/app/ai')
try:
    from email_guard import get_analyzer, get_model_info
    analyzer = get_analyzer()
    model_info = get_model_info()
    print(f'✓ Preloaded {len(analyzer.analyzers)} analyzers')
    print(f'✓ ML models loaded: {model_info.get(\"ml_models_loaded\", False)}')
    for analyzer_instance in analyzer.analyzers:
        print(f'  - {analyzer_instance.model_name} ({analyzer_instance.model_source})')
    
    # Test a simple analysis to ensure everything works
    test_results = analyzer.analyze_email('Test email for verification.')
    print(f'✓ Test analysis completed with {len(test_results)} results')
except Exception as e:
    print(f'✗ Failed to preload models: {e}')
    import traceback
    traceback.print_exc()
" > /tmp/model_loading.log 2>&1 &
MODEL_LOADING_PID=$!

echo "Model loading started in background (PID: $MODEL_LOADING_PID)"
echo "Server will start immediately while models load..."
echo "Model loading logs will be available in /tmp/model_loading.log"

# Start the application immediately
echo "Starting FastAPI server..."
exec uvicorn app:app --host 0.0.0.0 --port 8000
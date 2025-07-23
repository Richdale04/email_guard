#!/usr/bin/env python3
"""
Test script to verify model loading
"""

import sys
import os

# Add the ai directory to the path
sys.path.append('/app/ai')

def test_model_loading():
    """Test if models can be loaded"""
    print("Testing model loading...")
    
    try:
        from email_guard import get_analyzer, get_model_info
        
        print("✓ Successfully imported email_guard")
        
        # Get analyzer (this will trigger model loading)
        print("Loading analyzer...")
        analyzer = get_analyzer()
        print(f"✓ Analyzer loaded with {len(analyzer.analyzers)} analyzers")
        
        # List all analyzers
        for i, analyzer_instance in enumerate(analyzer.analyzers):
            print(f"  {i+1}. {analyzer_instance.model_name} ({analyzer_instance.model_source})")
            
            # Check if model is actually loaded
            if hasattr(analyzer_instance, 'model') and analyzer_instance.model is not None:
                print(f"     ✓ Model loaded")
            elif hasattr(analyzer_instance, 'detector') and analyzer_instance.detector is not None:
                print(f"     ✓ Detector loaded")
            elif hasattr(analyzer_instance, 'tokenizer') and analyzer_instance.tokenizer is not None:
                print(f"     ✓ Tokenizer loaded")
            else:
                print(f"     ✓ Available (rule-based)")
        
        # Get model info
        print("\nGetting model info...")
        model_info = get_model_info()
        print(f"✓ Model info retrieved:")
        print(f"  Total models: {model_info['total_models']}")
        print(f"  ML models loaded: {model_info['ml_models_loaded']}")
        print(f"  Primary ML available: {model_info['primary_ml_available']}")
        
        # Test a simple analysis
        print("\nTesting simple analysis...")
        test_email = "This is a test email for analysis."
        results = analyzer.analyze_email(test_email)
        print(f"✓ Analysis completed with {len(results)} results")
        
        for result in results:
            print(f"  - {result['model_name']}: {result['decision']} ({result['confidence']:.2f})")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model_loading()
    sys.exit(0 if success else 1) 
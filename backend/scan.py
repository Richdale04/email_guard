import sys
import os
from typing import List, Dict, Any
import json
from datetime import datetime

# Add the ai directory to the path to import email_guard
ai_path = '/app/ai'
sys.path.append(ai_path)


try:
    from email_guard import analyze_email_with_models
    print("âœ… Successfully imported email_guard")
except ImportError as e:
    print(f"âŒ Failed to import email_guard: {e}")
    # Fallback if email_guard is not available
    def analyze_email_with_models(email_text: str) -> List[Dict[str, Any]]:
        return []

def scan_email(email_text: str) -> List[Dict[str, Any]]:
    """
    Scan email text using multiple AI models
    
    Args:
        email_text: Sanitized email text to analyze
        
    Returns:
        List of model results with required fields
    """
    try:
        # Get results from AI models
        model_results = analyze_email_with_models(email_text)
        
        # Ensure all results have required fields
        validated_results = []
        for result in model_results:
            validated_result = {
                'model_source': result.get('model_source', 'unknown'),
                'model_name': result.get('model_name', 'unknown'),
                'decision': result.get('decision', 'unknown'),
                'confidence': float(result.get('confidence', 0.0)),
                'description': result.get('description', 'No description available')
            }
            validated_results.append(validated_result)
        
        # If no AI models are available, provide fallback analysis
        if not validated_results:
            validated_results = fallback_analysis(email_text)
        
        return validated_results
    
    except Exception as e:
        # Return error result if analysis fails
        return [{
            'model_source': 'system',
            'model_name': 'error_handler',
            'decision': 'error',
            'confidence': 0.0,
            'description': f'Analysis failed: {str(e)}'
        }]

def fallback_analysis(email_text: str) -> List[Dict[str, Any]]:
    """
    Fallback analysis when AI models are not available
    
    Args:
        email_text: Email text to analyze
        
    Returns:
        List of basic analysis results
    """
    from modules.verify import extract_email_metadata, detect_suspicious_patterns
    
    # Extract metadata
    metadata = extract_email_metadata(email_text.lower())
    suspicious_patterns = detect_suspicious_patterns(email_text)
    
    results = []
    
    # Basic rule-based analysis
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
    
    # Create result
    results.append({
        'model_source': 'rule_based',
        'model_name': 'basic_analyzer',
        'decision': decision,
        'confidence': confidence,
        'description': f'Risk score: {risk_score}/100. Factors: {", ".join(risk_factors) if risk_factors else "No suspicious patterns detected"}'
    })
    
    # Add metadata analysis
    results.append({
        'model_source': 'metadata',
        'model_name': 'content_analyzer',
        'decision': 'info',
        'confidence': 0.9,
        'description': f'Content analysis: {metadata["word_count"]} words, {metadata["char_count"]} characters, URLs: {metadata["has_urls"]}, Emails: {metadata["has_email_addresses"]}'
    })
    
    return results

def save_scan_history(user_id: str, email_text: str, results: List[Dict[str, Any]]) -> str:
    """
    Save scan results to history (for dashboard display)
    
    Args:
        user_id: User identifier
        email_text: Original email text
        results: Scan results
        
    Returns:
        History entry ID
    """
    # Create history directory if it doesn't exist
    history_dir = "backend/scan_history"
    os.makedirs(history_dir, exist_ok=True)
    
    # Create history entry
    history_entry = {
        'id': f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'user_id': user_id,
        'timestamp': datetime.now().isoformat(),
        'email_snippet': email_text[:200] + "..." if len(email_text) > 200 else email_text,
        'results': results
    }
    
    # Save to file
    history_file = os.path.join(history_dir, f"{history_entry['id']}.json")
    with open(history_file, 'w') as f:
        json.dump(history_entry, f, indent=2)
    
    return history_entry['id']

def get_scan_history(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get scan history for a user
    
    Args:
        user_id: User identifier
        limit: Maximum number of entries to return
        
    Returns:
        List of history entries
    """
    history_dir = "backend/scan_history"
    if not os.path.exists(history_dir):
        return []
    
    history_entries = []
    
    # Get all history files for the user
    for filename in os.listdir(history_dir):
        if filename.startswith(f"{user_id}_") and filename.endswith('.json'):
            try:
                with open(os.path.join(history_dir, filename), 'r') as f:
                    entry = json.load(f)
                    history_entries.append(entry)
            except (json.JSONDecodeError, FileNotFoundError):
                continue
    
    # Sort by timestamp (newest first) and limit results
    history_entries.sort(key=lambda x: x['timestamp'], reverse=True)
    return history_entries[:limit]
import sys
import os
from typing import List, Dict, Any
import json
from datetime import datetime

# Add the ai directory to the path to import email_guard
ai_path = '/app/ai'
sys.path.append(ai_path)

# Try to import email_guard
try:
    from email_guard import analyze_email_with_models
    print("Successfully imported email_guard")
    EMAIL_GUARD_AVAILABLE = True
except ImportError as e:
    print(f"Failed to import email_guard: {e}")
    EMAIL_GUARD_AVAILABLE = False

def scan_email(email_text: str) -> List[Dict[str, Any]]:
    """
    Scan email text using available AI models
    
    Args:
        email_text: Sanitized email text to analyze
        
    Returns:
        List of model results with required fields (only successful analyses)
    """
    try:
        # Only use email_guard if available
        if not EMAIL_GUARD_AVAILABLE:
            return []
        
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
        
        return validated_results
    
    except Exception as e:
        # Return empty list if analysis fails (no fallback)
        print(f"Email analysis failed: {e}")
        return []

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
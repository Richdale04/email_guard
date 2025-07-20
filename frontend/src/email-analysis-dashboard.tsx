import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './email-analysis-dashboard.css';

interface ModelResult {
  model_source: string;
  model_name: string;
  decision: string;
  confidence: number;
  description: string;
}

interface ScanResult {
  results: ModelResult[];
  timestamp: string;
  email_snippet: string;
}

interface HistoryEntry {
  id: string;
  user_id: string;
  timestamp: string;
  email_snippet: string;
  results: ModelResult[];
}

interface DashboardProps {
  currentScan?: ScanResult;
  onNewScan: () => void;
}

const EmailAnalysisDashboard: React.FC<DashboardProps> = ({ currentScan, onNewScan }) => {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:9080'}/history`, {
        withCredentials: true
      });

      if (response.status === 200) {
        setHistory(response.data.history || []);
      }
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Authentication required. Please log in again.');
      } else {
        setError('Failed to load history.');
      }
    } finally {
      setLoading(false);
    }
  };

  const getDecisionColor = (decision: string) => {
    switch (decision.toLowerCase()) {
      case 'phishing':
        return '#c53030';
      case 'spam':
        return '#d69e2e';
      case 'safe':
        return '#2f855a';
      case 'error':
        return '#718096';
      default:
        return '#4a5568';
    }
  };

  const getDecisionIcon = (decision: string) => {
    switch (decision.toLowerCase()) {
      case 'phishing':
        return '🚨';
      case 'spam':
        return '⚠️';
      case 'safe':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '❓';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const formatConfidence = (confidence: number) => {
    return `${(confidence * 100).toFixed(1)}%`;
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Email Analysis Dashboard</h1>
        <button onClick={onNewScan} className="new-scan-btn">
          New Analysis
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* Current Scan Results */}
      {currentScan && (
        <div className="current-scan-section">
          <h2>Latest Analysis Results</h2>
          <div className="email-snippet">
            <strong>Email Preview:</strong> {currentScan.email_snippet}
          </div>
          <div className="scan-timestamp">
            Analyzed: {formatTimestamp(currentScan.timestamp)}
          </div>
          
          <div className="results-grid">
            {currentScan.results.map((result, index) => (
              <div key={index} className="result-card">
                <div className="result-header">
                  <span className="decision-icon">
                    {getDecisionIcon(result.decision)}
                  </span>
                  <span 
                    className="decision-badge"
                    style={{ backgroundColor: getDecisionColor(result.decision) }}
                  >
                    {result.decision.toUpperCase()}
                  </span>
                </div>
                
                <div className="result-content">
                  <h3>{result.model_name}</h3>
                  <p className="model-source">Source: {result.model_source}</p>
                  <p className="confidence">
                    Confidence: {formatConfidence(result.confidence)}
                  </p>
                  <p className="description">{result.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* History Section */}
      <div className="history-section">
        <h2>Analysis History</h2>
        
        {loading ? (
          <div className="loading">Loading history...</div>
        ) : history.length === 0 ? (
          <div className="no-history">
            No previous analyses found. Start by analyzing an email!
          </div>
        ) : (
          <div className="history-list">
            {history.map((entry) => (
              <div key={entry.id} className="history-item">
                <div className="history-header">
                  <span className="history-timestamp">
                    {formatTimestamp(entry.timestamp)}
                  </span>
                  <span className="history-id">ID: {entry.id}</span>
                </div>
                
                <div className="history-email">
                  {entry.email_snippet}
                </div>
                
                <div className="history-results">
                  {entry.results.map((result, index) => (
                    <div key={index} className="history-result">
                      <span 
                        className="history-decision"
                        style={{ color: getDecisionColor(result.decision) }}
                      >
                        {getDecisionIcon(result.decision)} {result.decision.toUpperCase()}
                      </span>
                      <span className="history-model">{result.model_name}</span>
                      <span className="history-confidence">
                        {formatConfidence(result.confidence)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default EmailAnalysisDashboard; 
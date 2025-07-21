import React, { useState, useEffect } from 'react';
import axios from 'axios';

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
        return (
          <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 15.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        );
      case 'spam':
        return (
          <svg className="w-5 h-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'safe':
        return (
          <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      case 'error':
        return (
          <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        );
      default:
        return (
          <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const formatConfidence = (confidence: number) => {
    return `${(confidence * 100).toFixed(1)}%`;
  };

  return (
    <div className="min-h-screen bg-dark-950 py-12 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute top-0 left-0 w-full h-full bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%230ea5e9%22%20fill-opacity%3D%220.05%22%3E%3Ccircle%20cx%3D%2230%22%20cy%3D%2230%22%20r%3D%221%22%2F%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E')] opacity-50"></div>
      <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-neon-green/5 rounded-full blur-3xl"></div>
      <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-neon-blue/5 rounded-full blur-3xl"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-10 space-y-4 sm:space-y-0">
          <div>
            <h1 className="text-4xl font-bold text-dark-50 mb-3 text-shadow">Analysis Dashboard</h1>
            <p className="text-dark-300 text-lg">Monitor and review email security analysis results</p>
            <div className="w-32 h-1 bg-gradient-to-r from-cyber-500 to-neon-green mt-4 rounded-full"></div>
          </div>
          <button onClick={onNewScan} className="cyber-button flex items-center space-x-3 text-lg px-8 py-4">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            <span>New Analysis</span>
          </button>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-6 py-4 rounded-xl mb-8 text-sm">
            <div className="flex items-center space-x-3">
              <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Current Scan Results */}
        {currentScan && (
          <div className="cyber-card p-8 mb-10 relative">
            {/* Card Glow Effect */}
            <div className="absolute inset-0 bg-gradient-to-br from-cyber-500/5 to-neon-green/5 rounded-xl"></div>
            
            <div className="flex items-center space-x-4 mb-8 relative">
              <div className="w-12 h-12 bg-gradient-to-br from-neon-green to-cyber-500 rounded-xl flex items-center justify-center shadow-lg glow-green">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h2 className="text-2xl font-semibold text-dark-50">Latest Analysis Results</h2>
                <p className="text-dark-300">Real-time security assessment</p>
              </div>
            </div>
            
            <div className="cyber-card p-6 bg-dark-800/30 mb-6 relative">
              <div className="text-sm text-dark-400 mb-3 font-medium">Email Preview:</div>
              <div className="text-dark-200 font-mono text-sm leading-relaxed max-h-32 overflow-y-auto">
                {currentScan.email_snippet}
              </div>
            </div>
            
            <div className="text-sm text-dark-400 mb-8">
              <span className="inline-flex items-center space-x-3 bg-dark-800/50 px-4 py-2 rounded-lg">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Analyzed: {formatTimestamp(currentScan.timestamp)}</span>
              </span>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {currentScan.results.map((result, index) => (
                <div key={index} className="cyber-card p-6 bg-dark-800/50 hover:border-cyber-500/50 transition-all duration-200 relative group">
                  <div className="absolute inset-0 bg-gradient-to-br from-cyber-500/5 to-neon-green/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
                  
                  <div className="flex items-center justify-between mb-6 relative">
                    <div className="flex items-center space-x-3">
                      {getDecisionIcon(result.decision)}
                      <span className={`status-badge status-${result.decision.toLowerCase()}`}>
                        {result.decision}
                      </span>
                    </div>
                  </div>
                  
                  <div className="relative">
                    <h3 className="text-xl font-semibold text-dark-50 mb-3">{result.model_name}</h3>
                    <p className="text-sm text-dark-400 mb-4">Source: {result.model_source}</p>
                    <div className="flex items-center space-x-3 mb-4">
                      <span className="text-sm text-dark-300 font-medium">Confidence:</span>
                      <div className="flex-1 bg-dark-700 rounded-full h-3">
                        <div 
                          className="h-3 rounded-full bg-gradient-to-r from-cyber-500 to-neon-green transition-all duration-300"
                          style={{ width: `${result.confidence * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-semibold text-dark-200 min-w-[3rem]">{formatConfidence(result.confidence)}</span>
                    </div>
                    <p className="text-sm text-dark-300 leading-relaxed">{result.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* History Section */}
        <div className="cyber-card p-8 relative">
          {/* Card Glow Effect */}
          <div className="absolute inset-0 bg-gradient-to-br from-cyber-500/5 to-neon-green/5 rounded-xl"></div>
          
          <div className="flex items-center space-x-4 mb-8 relative">
            <div className="w-12 h-12 bg-gradient-to-br from-cyber-600 to-neon-purple rounded-xl flex items-center justify-center shadow-lg glow-blue">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h2 className="text-2xl font-semibold text-dark-50">Analysis History</h2>
              <p className="text-dark-300">Previous security assessments</p>
            </div>
          </div>
          
          {loading ? (
            <div className="text-center py-16">
              <div className="loading-spinner text-cyber-500 mx-auto mb-6 w-12 h-12"></div>
              <div className="text-dark-300 text-lg">Loading history...</div>
            </div>
          ) : history.length === 0 ? (
            <div className="text-center py-16">
              <svg className="w-20 h-20 text-dark-600 mx-auto mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <div className="text-dark-300 text-xl mb-3">No previous analyses found</div>
              <div className="text-dark-400">Start by analyzing an email to see your history here</div>
            </div>
          ) : (
            <div className="space-y-6">
              {history.map((entry) => (
                <div key={entry.id} className="cyber-card p-6 bg-dark-800/30 hover:border-dark-600/50 transition-all duration-200 relative group">
                  <div className="absolute inset-0 bg-gradient-to-br from-cyber-500/5 to-neon-green/5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
                  
                  <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 space-y-3 sm:space-y-0 relative">
                    <div className="flex items-center space-x-3">
                      <svg className="w-5 h-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span className="text-dark-200 font-semibold text-lg">
                        {formatTimestamp(entry.timestamp)}
                      </span>
                    </div>
                    <span className="text-dark-500 text-sm font-mono bg-dark-800/50 px-3 py-1 rounded-lg">ID: {entry.id}</span>
                  </div>
                  
                  <div className="cyber-card p-4 bg-dark-900/50 mb-6 relative">
                    <div className="text-dark-300 font-mono text-sm leading-relaxed max-h-24 overflow-y-auto">
                      {entry.email_snippet}
                    </div>
                  </div>
                  
                  <div className="flex flex-wrap gap-3">
                    {entry.results.map((result, index) => (
                      <div key={index} className="flex items-center space-x-3 bg-dark-700/50 px-4 py-3 rounded-xl text-sm border border-dark-600/30">
                        <div className="flex items-center space-x-2">
                          {getDecisionIcon(result.decision)}
                          <span className={`font-semibold ${
                            result.decision.toLowerCase() === 'phishing' ? 'text-red-400' :
                            result.decision.toLowerCase() === 'spam' ? 'text-yellow-400' :
                            result.decision.toLowerCase() === 'safe' ? 'text-green-400' :
                            'text-gray-400'
                          }`}>
                            {result.decision.toUpperCase()}
                          </span>
                        </div>
                        <span className="text-dark-400">•</span>
                        <span className="text-dark-300 font-medium">{result.model_name}</span>
                        <span className="text-dark-400">•</span>
                        <span className="text-dark-200 font-bold">
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
    </div>
  );
};

export default EmailAnalysisDashboard; 
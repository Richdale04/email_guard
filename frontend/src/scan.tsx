import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface ScanProps {
  onScanComplete: (results: any) => void;
}

const Scan: React.FC<ScanProps> = ({ onScanComplete }) => {
  const [emailText, setEmailText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [modelsReady, setModelsReady] = useState(false);
  const [checkingModels, setCheckingModels] = useState(true);

  // Check if models are ready on component mount and retry periodically
  useEffect(() => {
    const checkModelsStatus = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:9080'}/models/status`, {
          withCredentials: true
        });
        
        if (response.data.status === 'ready') {
          setModelsReady(true);
          setError('');
          return true; // Models are ready
        } else if (response.data.status === 'partial') {
          setModelsReady(true); // Allow analysis with rule-based models
          setError('Only rule-based models are available. ML models are still loading.');
          return true; // Partial models are ready
        } else {
          setError('AI models are not ready. Please wait a moment and try again.');
          return false; // Models not ready
        }
      } catch (err: any) {
        console.error('Failed to check models status:', err);
        setError('Unable to check AI models status. Please try again.');
        return false; // Error occurred
      } finally {
        setCheckingModels(false);
      }
    };

    // Initial check
    checkModelsStatus().then((modelsReady) => {
      // If models are not ready, retry every 10 seconds
      if (!modelsReady) {
        const interval = setInterval(async () => {
          const ready = await checkModelsStatus();
          if (ready) {
            clearInterval(interval);
          }
        }, 10000); // Retry every 10 seconds

        // Cleanup interval on unmount
        return () => clearInterval(interval);
      }
    });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:9080'}/scan/email`, {
        email_text: emailText
      }, {
        withCredentials: true,
        timeout: 300000 // 5 minutes timeout for cold start
      });

      if (response.status === 200) {
        onScanComplete(response.data);
      }
    } catch (err: any) {
      if (err.code === 'ECONNABORTED' || err.message.includes('timeout')) {
        setError('Request timed out. This may happen during the first analysis as AI models are loading. Please try again in a moment.');
      } else if (err.response?.status === 401) {
        setError('Authentication required. Please log in again.');
      } else if (err.response?.status === 504) {
        setError('Gateway timeout. The AI models may still be loading. Please wait a moment and try again.');
      } else if (err.response?.status === 503) {
        setError('AI models are not ready. Please wait a moment and try again.');
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Scan failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const loadSampleEmail = (type: 'phishing' | 'spam' | 'safe') => {
    const samples = {
      phishing: `Dear Customer,

Your account has been suspended due to suspicious activity detected on your account. 
This is URGENT and requires immediate attention.

Please click here to verify your identity and restore access:
http://secure-bank-verify.tk/account/verify

If you don't verify within 24 hours, your account will be permanently locked.

Best regards,
Bank Security Team`,
      
      spam: `CONGRATULATIONS! You've been selected for a LIMITED TIME OFFER!

Get 90% OFF on amazing products! 
Act now before this offer expires!

Click here to claim your discount:
http://amazing-offers.ga/discount

Don't miss this incredible opportunity!
Limited time only!`,
      
      safe: `Hi John,

Thanks for your email regarding the project update. I've reviewed the documents you sent and everything looks good.

Let's schedule a meeting next week to discuss the next steps. I'm available on Tuesday or Thursday afternoon.

Best regards,
Sarah`
    };

    setEmailText(samples[type]);
  };

  return (
    <div className="min-h-screen bg-dark-950 py-12 relative overflow-hidden">
      {/* Background Effects */}
      <div className="absolute top-0 left-0 w-full h-full bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%230ea5e9%22%20fill-opacity%3D%220.05%22%3E%3Ccircle%20cx%3D%2230%22%20cy%3D%2230%22%20r%3D%221%22%2F%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E')] opacity-50"></div>
      <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-neon-green/5 rounded-full blur-3xl"></div>
      <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-neon-blue/5 rounded-full blur-3xl"></div>
      
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="cyber-card p-8 relative">
          {/* Card Glow Effect */}
          <div className="absolute inset-0 bg-gradient-to-br from-cyber-500/5 to-neon-green/5 rounded-xl"></div>
          
          <div className="text-center mb-10 relative">
            <div className="flex justify-center mb-6">
              <div className="w-16 h-16 bg-gradient-to-br from-neon-green to-cyber-500 rounded-2xl flex items-center justify-center shadow-lg glow-green">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <h1 className="text-4xl font-bold text-dark-50 mb-3 text-shadow">Email Analysis</h1>
            <p className="text-dark-300 text-lg mb-4">Paste your email content below for AI-powered security analysis</p>
            {checkingModels && (
              <div className="bg-blue-500/10 border border-blue-500/30 text-blue-400 px-4 py-2 rounded-lg text-sm mb-4">
                <div className="flex items-center space-x-2">
                  <div className="loading-spinner w-4 h-4"></div>
                  <span>Checking AI models status...</span>
                </div>
              </div>
            )}
            {!checkingModels && !modelsReady && (
              <div className="bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 px-4 py-2 rounded-lg text-sm mb-4">
                <div className="flex items-center space-x-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                  <span>AI models are not ready. Please wait for them to load.</span>
                </div>
              </div>
            )}
            {modelsReady && error && error.includes('Only rule-based models') && (
              <div className="bg-orange-500/10 border border-orange-500/30 text-orange-400 px-4 py-2 rounded-lg text-sm mb-4">
                <div className="flex items-center space-x-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                  <span>Only rule-based models are available. ML models are still loading.</span>
                </div>
              </div>
            )}
            {modelsReady && !error && (
              <div className="bg-green-500/10 border border-green-500/30 text-green-400 px-4 py-2 rounded-lg text-sm mb-4">
                <div className="flex items-center space-x-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>AI models are ready for analysis!</span>
                </div>
              </div>
            )}
            <div className="w-32 h-1 bg-gradient-to-r from-cyber-500 to-neon-green mx-auto rounded-full"></div>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-8">
            <div>
              <label htmlFor="email-text" className="block text-sm font-medium text-dark-200 mb-4">
                Email Content
              </label>
              <div className="relative">
                <textarea
                  id="email-text"
                  className="cyber-textarea w-full h-80 font-mono text-sm"
                  value={emailText}
                  onChange={(e) => setEmailText(e.target.value)}
                  placeholder="Paste your email content here for analysis..."
                  required
                  disabled={loading}
                />
                <div className="absolute bottom-4 right-4 text-xs text-dark-400 bg-dark-800/50 px-2 py-1 rounded">
                  {emailText.length}/10,000 characters
                </div>
              </div>
            </div>
            
            <div className="cyber-card p-6 bg-dark-800/30">
              <p className="text-sm font-medium text-dark-200 mb-4">Try sample emails:</p>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <button 
                  type="button" 
                  onClick={() => loadSampleEmail('phishing')}
                  className="flex items-center justify-center space-x-3 bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-400 px-6 py-4 rounded-xl transition-all duration-200 text-sm font-medium hover:border-red-400/50 hover:shadow-lg hover:shadow-red-500/10"
                  disabled={loading}
                >
                  <span className="text-lg">🚨</span>
                  <span>Phishing Sample</span>
                </button>
                <button 
                  type="button" 
                  onClick={() => loadSampleEmail('spam')}
                  className="flex items-center justify-center space-x-3 bg-yellow-500/10 hover:bg-yellow-500/20 border border-yellow-500/30 text-yellow-400 px-6 py-4 rounded-xl transition-all duration-200 text-sm font-medium hover:border-yellow-400/50 hover:shadow-lg hover:shadow-yellow-500/10"
                  disabled={loading}
                >
                  <span className="text-lg">⚠️</span>
                  <span>Spam Sample</span>
                </button>
                <button 
                  type="button" 
                  onClick={() => loadSampleEmail('safe')}
                  className="flex items-center justify-center space-x-3 bg-green-500/10 hover:bg-green-500/20 border border-green-500/30 text-green-400 px-6 py-4 rounded-xl transition-all duration-200 text-sm font-medium hover:border-green-400/50 hover:shadow-lg hover:shadow-green-500/10"
                  disabled={loading}
                >
                  <span className="text-lg">✅</span>
                  <span>Safe Sample</span>
                </button>
              </div>
            </div>
            
            {error && (
              <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-6 py-4 rounded-xl text-sm">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{error}</span>
                  </div>
                  {!modelsReady && !checkingModels && (
                    <button
                      onClick={() => {
                        setCheckingModels(true);
                        setError('');
                        // Re-run the models status check
                        const checkModelsStatus = async () => {
                          try {
                            const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:9080'}/models/status`, {
                              withCredentials: true
                            });
                            
                            if (response.data.status === 'ready') {
                              setModelsReady(true);
                            } else {
                              setError('AI models are not ready. Please wait a moment and try again.');
                            }
                          } catch (err: any) {
                            console.error('Failed to check models status:', err);
                            setError('Unable to check AI models status. Please try again.');
                          } finally {
                            setCheckingModels(false);
                          }
                        };
                        checkModelsStatus();
                      }}
                      className="bg-red-500/20 hover:bg-red-500/30 border border-red-500/40 text-red-300 px-3 py-1 rounded text-xs transition-colors"
                    >
                      Retry
                    </button>
                  )}
                </div>
              </div>
            )}
            
            <button 
              type="submit" 
              className={`cyber-button w-full flex items-center justify-center space-x-4 text-xl py-6 ${loading ? 'scan-animation' : ''}`}
              disabled={loading || !emailText.trim() || !modelsReady || checkingModels}
            >
              {loading ? (
                <>
                  <div className="loading-spinner"></div>
                  <span>Analyzing Email...</span>
                </>
              ) : checkingModels ? (
                <>
                  <div className="loading-spinner"></div>
                  <span>Checking AI Models...</span>
                </>
              ) : !modelsReady ? (
                <>
                  <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                  <span>AI Models Not Ready</span>
                </>
              ) : (
                <>
                  <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>Analyze Email</span>
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Scan; 
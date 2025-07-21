import React, { useState, useEffect } from 'react';
import Auth from './auth';
import Scan from './scan';
import EmailAnalysisDashboard from './email-analysis-dashboard';
import axios from 'axios';

type AppState = 'auth' | 'scan' | 'dashboard';

interface ScanResult {
  results: Array<{
    model_source: string;
    model_name: string;
    decision: string;
    confidence: number;
    description: string;
  }>;
  timestamp: string;
  email_snippet: string;
}

function App() {
  const [currentState, setCurrentState] = useState<AppState>('auth');
  const [currentScan, setCurrentScan] = useState<ScanResult | undefined>();
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  // Load saved state and check auth on app load
  useEffect(() => {
    const initializeApp = async () => {
      // First, load saved state from localStorage
      const savedState = localStorage.getItem('emailGuardState');
      const savedScan = localStorage.getItem('emailGuardScan');
      
      if (savedState && savedState !== 'auth') {
        setCurrentState(savedState as AppState);
      }
      
      if (savedScan) {
        try {
          setCurrentScan(JSON.parse(savedScan));
        } catch (e) {
          // If parsing fails, ignore the saved scan
        }
      }
      
      // Then check authentication status
      await checkAuthStatus();
    };

    initializeApp();
  }, []);

  // Save state to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('emailGuardState', currentState);
  }, [currentState]);

  // Save scan results to localStorage
  useEffect(() => {
    if (currentScan) {
      localStorage.setItem('emailGuardScan', JSON.stringify(currentScan));
    } else {
      localStorage.removeItem('emailGuardScan');
    }
  }, [currentScan]);

  const checkAuthStatus = async () => {
    try {
      // Try to make a request to check if the user is authenticated
      const response = await axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:9080'}/health`, {
        withCredentials: true
      });
      
      // If authenticated, keep current state (don't change anything)
      // The saved state from localStorage will be preserved
      
    } catch (err: any) {
      // If not authenticated, go to auth page and clear saved state
      setCurrentState('auth');
      setCurrentScan(undefined);
      localStorage.removeItem('emailGuardState');
      localStorage.removeItem('emailGuardScan');
    } finally {
      setIsCheckingAuth(false);
    }
  };

  const handleAuthSuccess = () => {
    setCurrentState('scan');
  };

  const handleScanComplete = (results: ScanResult) => {
    setCurrentScan(results);
    setCurrentState('dashboard');
  };

  const handleNewScan = () => {
    setCurrentScan(undefined);
    setCurrentState('scan');
  };

  const handleLogout = async () => {
    try {
      // Call backend to clear the HTTP-only cookie
      await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:9080'}/auth/logout`, {}, {
        withCredentials: true
      });
    } catch (error) {
      // Ignore errors on logout
    }
    
    // Clear local state
    setCurrentState('auth');
    setCurrentScan(undefined);
    localStorage.removeItem('emailGuardState');
    localStorage.removeItem('emailGuardScan');
  };

  const renderHeader = () => {
    if (currentState === 'auth') return null;
    
    return (
      <div className="sticky top-0 z-50 bg-dark-900/90 backdrop-blur-xl border-b border-dark-700/50 shadow-2xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-br from-cyber-500 to-neon-green rounded-xl flex items-center justify-center shadow-lg glow-green">
                <span className="text-white font-bold text-sm">EG</span>
              </div>
              <div>
                <span className="text-dark-100 font-bold text-xl">Email Guard</span>
                <div className="text-xs text-dark-400 font-medium">
                  {currentState === 'scan' ? 'Security Analysis' : 'Dashboard'}
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="hidden sm:flex items-center space-x-2 text-sm text-dark-400">
                <div className="w-2 h-2 bg-neon-green rounded-full animate-pulse"></div>
                <span>System Online</span>
              </div>
              <button 
                onClick={handleLogout} 
                className="cyber-button-danger text-sm px-4 py-2 flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderCurrentComponent = () => {
    if (isCheckingAuth) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-dark-950 relative overflow-hidden">
          {/* Background Effects */}
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-neon-green/5 rounded-full blur-3xl animate-pulse-slow"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-neon-blue/5 rounded-full blur-3xl animate-pulse-slow" style={{animationDelay: '1s'}}></div>
          
          <div className="flex flex-col items-center space-y-6 relative z-10">
            <div className="w-16 h-16 bg-gradient-to-br from-cyber-500 to-neon-green rounded-2xl flex items-center justify-center shadow-lg glow-green">
              <div className="loading-spinner text-white w-8 h-8"></div>
            </div>
            <div className="text-center">
              <div className="text-dark-100 font-semibold text-lg mb-2">Initializing Security System</div>
              <div className="text-dark-400 text-sm">Loading AI models and security protocols...</div>
            </div>
          </div>
        </div>
      );
    }

    switch (currentState) {
      case 'auth':
        return <Auth onAuthSuccess={handleAuthSuccess} />;
      case 'scan':
        return (
          <div className="min-h-screen bg-dark-950">
            {renderHeader()}
            <Scan onScanComplete={handleScanComplete} />
          </div>
        );
      case 'dashboard':
        return (
          <div className="min-h-screen bg-dark-950">
            {renderHeader()}
            <EmailAnalysisDashboard
              currentScan={currentScan}
              onNewScan={handleNewScan}
            />
          </div>
        );
      default:
        return <Auth onAuthSuccess={handleAuthSuccess} />;
    }
  };

  return (
    <div className="App">
      {renderCurrentComponent()}
    </div>
  );
}

export default App;

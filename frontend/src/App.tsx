import React, { useState, useEffect } from 'react';
import Auth from './auth';
import Scan from './scan';
import EmailAnalysisDashboard from './email-analysis-dashboard';
import axios from 'axios';
import './App.css';

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

  const renderCurrentComponent = () => {
    if (isCheckingAuth) {
      return (
        <div className="loading-container">
          <div className="loading-spinner">Loading...</div>
        </div>
      );
    }

    switch (currentState) {
      case 'auth':
        return <Auth onAuthSuccess={handleAuthSuccess} />;
      case 'scan':
        return (
          <div>
            <div className="header-bar">
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
            <Scan onScanComplete={handleScanComplete} />
          </div>
        );
      case 'dashboard':
        return (
          <div>
            <div className="header-bar">
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
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

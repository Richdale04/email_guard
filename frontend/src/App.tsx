import React, { useState } from 'react';
import Auth from './auth';
import Scan from './scan';
import EmailAnalysisDashboard from './email-analysis-dashboard';
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

  const renderCurrentComponent = () => {
    switch (currentState) {
      case 'auth':
        return <Auth onAuthSuccess={handleAuthSuccess} />;
      case 'scan':
        return <Scan onScanComplete={handleScanComplete} />;
      case 'dashboard':
        return (
          <EmailAnalysisDashboard
            currentScan={currentScan}
            onNewScan={handleNewScan}
          />
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

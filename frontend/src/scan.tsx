import React, { useState } from 'react';
import axios from 'axios';
import './scan.css';

interface ScanProps {
  onScanComplete: (results: any) => void;
}

const Scan: React.FC<ScanProps> = ({ onScanComplete }) => {
  const [emailText, setEmailText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:9080'}/scan/email`, {
        email_text: emailText
      }, {
        withCredentials: true
      });

      if (response.status === 200) {
        onScanComplete(response.data);
      }
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Authentication required. Please log in again.');
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
    <div className="scan-container">
      <div className="scan-card">
        <div className="scan-header">
          <h1>Email Analysis</h1>
          <p>Paste your email content below for AI-powered security analysis</p>
        </div>
        
        <form onSubmit={handleSubmit} className="scan-form">
          <div className="form-group">
            <label htmlFor="email-text">Email Content</label>
            <textarea
              id="email-text"
              value={emailText}
              onChange={(e) => setEmailText(e.target.value)}
              placeholder="Paste your email content here..."
              rows={12}
              required
              disabled={loading}
            />
            <div className="char-count">
              {emailText.length}/10,000 characters
            </div>
          </div>
          
          <div className="sample-emails">
            <p>Try sample emails:</p>
            <div className="sample-buttons">
              <button 
                type="button" 
                onClick={() => loadSampleEmail('phishing')}
                className="sample-btn phishing"
                disabled={loading}
              >
                Phishing Sample
              </button>
              <button 
                type="button" 
                onClick={() => loadSampleEmail('spam')}
                className="sample-btn spam"
                disabled={loading}
              >
                Spam Sample
              </button>
              <button 
                type="button" 
                onClick={() => loadSampleEmail('safe')}
                className="sample-btn safe"
                disabled={loading}
              >
                Safe Sample
              </button>
            </div>
          </div>
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          <button 
            type="submit" 
            className="scan-button"
            disabled={loading || !emailText.trim()}
          >
            {loading ? 'Analyzing...' : 'Analyze Email'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Scan; 
import React, { useState } from 'react';
import axios from 'axios';
import './auth.css';

interface AuthProps {
  onAuthSuccess: () => void;
}

const Auth: React.FC<AuthProps> = ({ onAuthSuccess }) => {
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:9080'}/auth/token`, {
        token: token
      }, {
        withCredentials: true
      });

      if (response.status === 200) {
        onAuthSuccess();
      }
    } catch (err: any) {
      if (err.response?.status === 429) {
        setError('Too many authentication attempts. Please wait 7 minutes before trying again.');
      } else if (err.response?.status === 401) {
        setError('Invalid token. Please check your token and try again.');
      } else {
        setError('Authentication failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Email Guard</h1>
          <p>AI-Powered Email Security Analysis</p>
        </div>
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="token">Enter Your Access Token</label>
            <input
              type="password"
              id="token"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              placeholder="Enter your purchased token"
              required
              disabled={loading}
            />
          </div>
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          <button 
            type="submit" 
            className="auth-button"
            disabled={loading || !token.trim()}
          >
            {loading ? 'Authenticating...' : 'Authenticate'}
          </button>
        </form>
        
        <div className="auth-footer">
          <p>Don't have a token? Contact us to purchase access.</p>
          <p className="demo-info">
            <strong>Demo Tokens:</strong><br/>
            • sample_token_1 (User)<br/>
            • sample_token_2 (Admin)
          </p>
        </div>
      </div>
    </div>
  );
};

export default Auth; 
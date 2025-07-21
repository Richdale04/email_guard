import React, { useState } from 'react';
import axios from 'axios';

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
    <div className="min-h-screen bg-dark-950 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated Background Pattern */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg%20width%3D%2260%22%20height%3D%2260%22%20viewBox%3D%220%200%2060%2060%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20fill%3D%22none%22%20fill-rule%3D%22evenodd%22%3E%3Cg%20fill%3D%22%230ea5e9%22%20fill-opacity%3D%220.1%22%3E%3Ccircle%20cx%3D%2230%22%20cy%3D%2230%22%20r%3D%221%22%2F%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E')] opacity-30 animate-pulse-slow"></div>
      
      {/* Glow Effects */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-neon-green/10 rounded-full blur-3xl animate-glow"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-neon-blue/10 rounded-full blur-3xl animate-glow" style={{animationDelay: '1s'}}></div>
      
      <div className="relative w-full max-w-md z-10">
        {/* Main Card */}
        <div className="cyber-card p-8 relative">
          {/* Card Glow Effect */}
          <div className="absolute inset-0 bg-gradient-to-br from-cyber-500/5 to-neon-green/5 rounded-xl"></div>
          
          {/* Header */}
          <div className="text-center mb-8 relative">
            {/* Logo */}
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-cyber-500 to-neon-green rounded-2xl mb-6 shadow-lg glow-green">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            
            {/* Title */}
            <h1 className="text-3xl font-bold text-dark-50 mb-3 text-shadow">Email Guard</h1>
            <p className="text-dark-300 text-lg">AI-Powered Email Security Analysis</p>
            <div className="w-24 h-1 bg-gradient-to-r from-cyber-500 to-neon-green mx-auto mt-4 rounded-full"></div>
          </div>
          
          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6 relative">
            <div>
              <label htmlFor="token" className="block text-sm font-medium text-dark-200 mb-3">
                Access Token
              </label>
              <input
                type="password"
                id="token"
                className="cyber-input w-full"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="Enter your security token"
                required
                disabled={loading}
              />
            </div>
            
            {/* Error Message */}
            {error && (
              <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg text-sm">
                <div className="flex items-center space-x-2">
                  <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{error}</span>
                </div>
              </div>
            )}
            
            {/* Submit Button */}
            <button 
              type="submit" 
              className="cyber-button w-full text-lg py-4"
              disabled={loading || !token.trim()}
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-3">
                  <div className="loading-spinner"></div>
                  <span>Authenticating...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center space-x-3">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                  </svg>
                  <span>Authenticate</span>
                </div>
              )}
            </button>
          </form>
          
          {/* Footer */}
          <div className="mt-8 pt-6 border-t border-dark-700/50 text-center">
            <p className="text-dark-400 text-sm">
              Don't have a token? 
              <button className="text-cyber-400 hover:text-neon-green ml-1 transition-colors duration-200 underline decoration-dotted">
                Contact us for access
              </button>
            </p>
          </div>
        </div>
        
        {/* Bottom Glow Effect */}
        <div className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 w-3/4 h-8 bg-gradient-to-r from-cyber-500/20 to-neon-green/20 blur-xl rounded-full"></div>
      </div>
    </div>
  );
};

export default Auth;
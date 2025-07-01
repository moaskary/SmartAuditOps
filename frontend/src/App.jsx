
import { useState } from 'react';
import axios from 'axios';
import './App.css'; 

function App() {
  const [snippet, setSnippet] = useState('');
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAudit = async () => {
    if (!snippet) {
      setError('Please enter a code snippet to analyze.');
      return;
    }
    
    setIsLoading(true);
    setError('');
    setResults(null);

    try {
      const API_URL = '/api/audit/code';
      
      const response = await axios.post(API_URL, {
        snippet: snippet,
        language: 'python' 
      });
      
      setResults(response.data.results.analysis);

    } catch (err) {
      console.error("Error auditing code:", err);
      setError('Failed to get analysis. Is the backend running?');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>🚀 SmartAuditOps</h1>
        <p>AI-Powered Code, Security, and Compliance Reviewer</p>
      </header>

      <div className="audit-section">
        <textarea
          value={snippet}
          onChange={(e) => setSnippet(e.target.value)}
          placeholder="Paste your code snippet here..."
          rows="10"
        />
        <button onClick={handleAudit} disabled={isLoading}>
          {isLoading ? 'Analyzing...' : 'Analyze Snippet'}
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}

      {results && (
        <div className="results-section">
          <h2>Analysis Results</h2>
          <ul>
            {Object.entries(results).map(([label, score]) => (
              <li key={label}>
                <span>{label}</span>
                <div className="score-bar-container">
                  <div 
                    className="score-bar" 
                    style={{ width: `${score * 100}%`, backgroundColor: score > 0.8 ? '#e53e3e' : '#4299e1' }}
                  ></div>
                </div>
                <span>{(score * 100).toFixed(2)}%</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
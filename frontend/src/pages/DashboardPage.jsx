// frontend/src/pages/DashboardPage.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import '../App.css'

// Helper function to find the highest risk in a result
const getTopIssue = (result) => {
  if (!result || !result.analysis) return { label: 'N/A', score: 0 };
  return Object.entries(result.analysis).reduce((top, [label, score]) => {
    return score > top.score ? { label, score } : top;
  }, { label: '', score: 0.0 });
};

// Helper function to process data for the chart
const processChartData = (audits) => {
    const issueCounts = audits.reduce((acc, audit) => {
        const topIssue = getTopIssue(audit.results);
        if (topIssue.score > 0.5 && topIssue.label !== 'safe code') { // Only count significant non-safe issues
            acc[topIssue.label] = (acc[topIssue.label] || 0) + 1;
        }
        return acc;
    }, {});

    return Object.entries(issueCounts).map(([name, count]) => ({ name, count }));
};

function DashboardPage() {
  const [audits, setAudits] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAudits = async () => {
      try {
        const response = await axios.get('/api/audit/');
        setAudits(response.data);
      } catch (err) {
        setError('Failed to fetch audit history.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchAudits();
  }, []); // Empty array means this runs once on component mount

  if (isLoading) return <p>Loading dashboard...</p>;
  if (error) return <p className="error-message">{error}</p>;

  const chartData = processChartData(audits);

  return (
    <div>
      <header>
        <h1>DevOps Dashboard</h1>
        <p>Overview of historical code audits.</p>
      </header>
      
      <div className="chart-container">
        <h2>Issue Types by Frequency</h2>
        <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#e53e3e" />
            </BarChart>
        </ResponsiveContainer>
      </div>

      <h2>Audit History</h2>
      <table className="audit-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Timestamp</th>
            <th>Top Issue</th>
            <th>Score</th>
            <th>Snippet</th>
          </tr>
        </thead>
        <tbody>
          {audits.map((audit) => {
            const topIssue = getTopIssue(audit.results);
            return (
              <tr key={audit.id}>
                <td>{audit.id}</td>
                <td>{new Date(audit.timestamp).toLocaleString()}</td>
                <td>{topIssue.label}</td>
                <td>{(topIssue.score * 100).toFixed(1)}%</td>
                <td><pre><code>{audit.snippet.substring(0, 100)}...</code></pre></td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default DashboardPage;
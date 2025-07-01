// frontend/src/App.jsx
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import AuditPage from './pages/AuditPage';
import DashboardPage from './pages/DashboardPage'; // We will create this next
import './App.css';

function App() {
  return (
    <Router>
      <div className="container">
        <nav className="main-nav">
          <Link to="/">Audit Snippet</Link>
          <Link to="/dashboard">Dashboard</Link>
        </nav>
        <main>
          <Routes>
            <Route path="/" element={<AuditPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
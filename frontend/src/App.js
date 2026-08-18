import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import TestRunnerPage from './TestRunnerPage';
import AnalyticsPage from './AnalyticsPage';

function App() {
  return (
    <Router>
      <div className="container mt-4">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4 px-3 rounded shadow-sm">
          <span className="navbar-brand">Performance Platform</span>
          <div className="navbar-nav">
            <Link className="nav-link" to="/">Test Runner Form</Link>
            <Link className="nav-link" to="/analytics">Analytics & PDF</Link>
          </div>
        </nav>
        <Routes>
          <Route path="/" element={<TestRunnerPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
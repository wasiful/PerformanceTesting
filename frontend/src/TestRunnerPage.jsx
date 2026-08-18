import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function TestRunnerPage() {
  const [config, setConfig] = useState({ url: 'https://httpbin.org/get', test_type: 'Load', users: 5, duration: 10 });
  const [activeRunId, setActiveRunId] = useState(null);
  const [runDetails, setRunDetails] = useState(null);
  const [loading, setLoading] = useState(false);

  const startTest = async () => {
    setLoading(true);
    setRunDetails(null);
    try {
      const res = await axios.post('http://127.0.0.1:8000/run-test', config);
      setActiveRunId(res.data.test_run_id);
    } catch (err) {
      alert(`Error starting test: ${err.message}`);
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!activeRunId) return;
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/run/${activeRunId}`);
        setRunDetails(res.data);
        if (res.data.status === 'COMPLETED' || res.data.status === 'FAILED') {
          setLoading(false);
          clearInterval(interval);
        }
      } catch (err) {
        clearInterval(interval);
        setLoading(false);
      }
    }, 1500);
    return () => clearInterval(interval);
  }, [activeRunId]);

  return (
    <div className="card p-4 shadow-sm">
      <h3 className="mb-3">Configure & Execute Test</h3>
      <div className="row g-3">
        <div className="col-12">
          <label className="form-label">Target URL:</label>
          <input className="form-control" value={config.url} onChange={e => setConfig({...config, url: e.target.value})} />
        </div>
        <div className="col-md-4">
          <label className="form-label">Test Suite Category:</label>
          <select className="form-select" value={config.test_type} onChange={e => setConfig({...config, test_type: e.target.value})}>
            <option>Load</option>
            <option>Soak</option>
            <option>Stress</option>
            <option>Spike</option>
            <option>Volume</option>
            <option>Failover</option>
          </select>
        </div>
        <div className="col-md-4">
          <label className="form-label">Concurrent Users:</label>
          <input type="number" className="form-control" value={config.users} onChange={e => setConfig({...config, users: parseInt(e.target.value) || 1})} />
        </div>
        <div className="col-md-4">
          <label className="form-label">Duration (Seconds):</label>
          <input type="number" className="form-control" value={config.duration} onChange={e => setConfig({...config, duration: parseInt(e.target.value) || 1})} />
        </div>
      </div>

      <div className="mt-4">
        <button className="btn btn-primary" onClick={startTest} disabled={loading}>
          {loading ? 'Running Test Suite...' : 'Start Execution'}
        </button>
      </div>

      {runDetails && (
        <div className="mt-4 alert alert-secondary">
          <h5>Status: <span className="badge bg-info">{runDetails.status}</span></h5>
          {runDetails.status === 'COMPLETED' && (
            <div className="mt-2">
              <p className="mb-1">Total Requests Sent: <strong>{runDetails.total_requests}</strong></p>
              <p className="mb-2">Success Rate: <strong>{runDetails.success_count} / {runDetails.total_requests}</strong></p>
              <a className="btn btn-success" href={`http://127.0.0.1:8000/export-csv/${runDetails.id}`} target="_blank" rel="noreferrer">
                Download Generated CSV
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
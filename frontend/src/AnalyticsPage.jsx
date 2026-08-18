import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function AnalyticsPage() {
  const [runs, setRuns] = useState([]);
  const [selectedRunId, setSelectedRunId] = useState('');
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/runs').then(res => {
      setRuns(res.data);
      if (res.data.length > 0) setSelectedRunId(res.data[0].id);
    });
  }, []);

  useEffect(() => {
    if (!selectedRunId) return;
    axios.get(`http://127.0.0.1:8000/analytics-data/${selectedRunId}`).then(res => {
      const records = res.data.results;
      setChartData({
        labels: records.map(r => `Req ${r.seq}`),
        datasets: [
          {
            label: 'Response Time (ms)',
            data: records.map(r => r.time_ms),
            borderColor: '#0d6efd',
            backgroundColor: 'rgba(13, 110, 253, 0.2)',
            tension: 0.1
          }
        ]
      });
    }).catch(() => setChartData(null));
  }, [selectedRunId]);

  const downloadPDF = () => {
    if (selectedRunId) {
      window.open(`http://127.0.0.1:8000/generate-pdf/${selectedRunId}`);
    }
  };

  return (
    <div className="card p-4 shadow-sm">
      <h3 className="mb-3">Analytics & Visualizations</h3>
      
      <div className="row mb-4">
        <div className="col-md-6">
          <label className="form-label">Select Test Run History:</label>
          <select className="form-select" value={selectedRunId} onChange={e => setSelectedRunId(e.target.value)}>
            {runs.map(r => (
              <option key={r.id} value={r.id}>
                Run #{r.id} - {r.test_type} ({r.target_url}) - {r.status}
              </option>
            ))}
          </select>
        </div>
        <div className="col-md-6 d-flex align-items-end">
          <button className="btn btn-danger" onClick={downloadPDF} disabled={!selectedRunId}>
            Export PDF Analytics Report
          </button>
        </div>
      </div>

      {chartData ? (
        <div className="p-3 border rounded">
          <Line data={chartData} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />
        </div>
      ) : (
        <p className="text-muted">Select a completed test run to view latency trends.</p>
      )}
    </div>
  );
}
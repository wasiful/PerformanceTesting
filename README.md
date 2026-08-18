This application performs Performance Testing. Load, Soak, Spike, Stress, Volume, Failover Tests.
It will provide the graphs.

Change all the directories according to your own device directories,
First run the install dependencies ps1 file then run the start the test ps1 file
it will use uv and npm
and it will open up a browser for you to select the test type and your parameters.


System Architecture and Execution Flow

Triggering the Test

The React UI running on Port 3000 sends an HTTP POST request to the run test endpoint on the FastAPI Web Server running on Port 8000. FastAPI immediately responds with an HTTP 200 OK status code along with a generated test run ID to ensure the client remains non-blocking.

Background Execution

The FastAPI Background Tasks system triggers a ThreadPoolExecutor configured with concurrent worker threads. These worker threads continuously fire HTTP GET load requests directly to the Target Server.

Data Aggregation and Telemetry

All test results are aggregated and persisted across multiple storage layers. Raw metrics are written to the SQLite database performance.db file. Detailed raw request records are exported into CSV files. Visual summary analytics are compiled into downloadable PDF reports.

UI Updates and Visualization

The React UI periodically polls the run status endpoint every 1.5 seconds. Upon test completion, the frontend fetches the complete dataset to render an Interactive Latency Graph for user analytics.

Directory Structure

Root Folder

The root directory located at D:\autodev\performancetester contains the requirements.txt file for Python package dependencies and the performance.db file which serves as the local SQLite database auto-generated on application startup.

Backend Services

The backend folder contains main.py for API endpoints and background task routing. The database.py file handles the SQLAlchemy connection and session creation. The models.py file establishes ORM definitions including TestRun and RequestResult. The exports folder stores generated CSV and PDF output files. Inside backend tests, test_runner.py houses the concurrent load testing execution engine. Inside backend reports, pdf_generator.py provides the PDF report compilation and charting engine.

Frontend Interface

The frontend src folder contains App.js for main client routing and navigation. TestRunnerPage.jsx handles the test configuration form input and status polling logic. AnalyticsPage.jsx provides the historical analytics dashboard, Chart.js graphical views, and PDF export triggers.


Navigate to http://localhost:3000 in your browser.

Enter a Target URL (e.g., [https://httpbin.org/get](https://httpbin.org/get)), select concurrency levels (Users) and duration, then click Start Execution.

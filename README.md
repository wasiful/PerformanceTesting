This application performs Performance Testing. Load, Soak, Spike, Stress, Volume, Failover Tests.
It will provide the graphs.

Change all the directories according to your own device directories,
First run the install dependencies ps1 file then run the start the test ps1 file
it will use uv and npm
and it will open up a browser for you to select the test type and your parameters.


┌─────────────────┐       HTTP POST /run-test       ┌────────────────────────┐
│                 │ ──────────────────────────────> │                        │
│   React UI      │                                 │   FastAPI Web Server   │
│  (Port 3000)    │ <────────────────────────────── │      (Port 8000)       │
└─────────────────┘      200 OK + test_run_id       └────────────────────────┘
         │                                                      │
         │ Poll /run/{id}                                       │ FastAPI BackgroundTasks
         ▼ (Every 1.5s)                                         ▼
┌─────────────────┐                        ┌─────────────────────────────────┐
│                 │                        │     ThreadPoolExecutor          │
│   Interactive   │                        │   (Concurrent Worker Threads)   │
│  Latency Graph  │                        └─────────────────────────────────┘
└─────────────────┘                                         │
                                                            │ Fires HTTP GET Requests
                                                            ▼
                                                    ┌───────────────┐
                                                    │ Target Server │
                                                    └───────────────┘
                                                            │
                                                            │ Aggregates & Persists
                                                            ▼
                                           ┌─────────────────────────────────┐
                                           │  • SQLite DB (performance.db)   │
                                           │  • CSV Exports (.csv)           │
                                           │  • PDF Reports (.pdf)           │
                                           └─────────────────────────────────┘


D:\autodev\performancetester
├── requirements.txt                # Python environment package list
├── performance.db                  # Local SQLite database (Auto-generated on startup)
├── backend/
│   ├── main.py                     # FastAPI application endpoints & BackgroundTask routing
│   ├── database.py                 # SQLAlchemy SQLite engine connection & session generator
│   ├── models.py                   # ORM models (TestRun, RequestResult)
│   ├── exports/                    # Output directory for generated CSV & PDF reports
│   ├── tests/
│   │   └── test_runner.py          # Concurrent ThreadPoolExecutor load generator
│   └── reports/
│       └── pdf_generator.py        # ReportLab PDF compiler & Matplotlib charting script
└── frontend/
    └── src/
        ├── App.js                  # Main React routing and navigation bar
        ├── TestRunnerPage.jsx      # Test configuration form & status poller
        └── AnalyticsPage.jsx       # Historical runs viewer, Chart.js graphs, & PDF export trigger


Navigate to http://localhost:3000 in your browser.

Enter a Target URL (e.g., [https://httpbin.org/get](https://httpbin.org/get)), select concurrency levels (Users) and duration, then click Start Execution.

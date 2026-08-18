import os
import pandas as pd
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import init_db, get_db, SessionLocal
from models import TestRun, RequestResult
from tests.test_runner import execute_test_suite
from reports.pdf_generator import generate_analytics_report

app = FastAPI(title="Performance Testing Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestConfigSchema(BaseModel):
    url: str
    test_type: str = "Load"
    users: int = 10
    duration: int = 10

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"status": "Performance Testing API Active", "docs": "/docs"}

@app.post("/run-test")
def start_test(config: TestConfigSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    new_run = TestRun(
        target_url=config.url,
        test_type=config.test_type,
        users=config.users,
        duration_sec=config.duration,
        status="PENDING"
    )
    db.add(new_run)
    db.commit()
    db.refresh(new_run)
    
    # Execute test loop asynchronously in background thread
    background_tasks.add_task(execute_test_suite, new_run.id, SessionLocal)
    
    return {"message": "Test initialized", "test_run_id": new_run.id, "status": "PENDING"}

@app.get("/runs")
def list_runs(db: Session = Depends(get_db)):
    runs = db.query(TestRun).order_by(TestRun.id.desc()).all()
    return runs

@app.get("/run/{run_id}")
def get_run_status(run_id: int, db: Session = Depends(get_db)):
    run = db.query(TestRun).filter(TestRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@app.get("/export-csv/{run_id}")
def export_csv(run_id: int, db: Session = Depends(get_db)):
    run = db.query(TestRun).filter(TestRun.id == run_id).first()
    if not run or not run.csv_file_path or not os.path.exists(run.csv_file_path):
        raise HTTPException(status_code=404, detail="CSV report not available")
    return FileResponse(run.csv_file_path, filename=f"test_run_{run_id}.csv", media_type="text/csv")

@app.get("/analytics-data/{run_id}")
def get_analytics_data(run_id: int, db: Session = Depends(get_db)):
    results = db.query(RequestResult).filter(RequestResult.test_run_id == run_id).order_by(RequestResult.sequence).all()
    if not results:
        raise HTTPException(status_code=404, detail="No analytics records found for this run")
    
    data = [{
        "seq": r.sequence,
        "time_ms": r.request_time_ms,
        "status": r.status_code,
        "success": r.success
    } for r in results]
    
    return {"run_id": run_id, "results": data}

@app.post("/generate-pdf/{run_id}")
def generate_pdf_from_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(TestRun).filter(TestRun.id == run_id).first()
    if not run or not run.csv_file_path or not os.path.exists(run.csv_file_path):
        raise HTTPException(status_code=404, detail="Run CSV file missing")
    
    pdf_path = run.csv_file_path.replace(".csv", ".pdf")
    generate_analytics_report(run.csv_file_path, pdf_path)
    return FileResponse(pdf_path, filename=f"Analytics_Report_{run_id}.pdf", media_type="application/pdf")
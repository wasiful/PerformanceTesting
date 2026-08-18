import time
import os
import concurrent.futures
import requests
import pandas as pd
import datetime
from sqlalchemy.orm import Session
from models import TestRun, RequestResult

def send_request(url: str, seq: int):
    start = time.time()
    try:
        response = requests.get(url, timeout=10)
        elapsed = (time.time() - start) * 1000
        return {
            "sequence": seq,
            "success": response.status_code < 400,
            "status_code": response.status_code,
            "request_time_ms": round(elapsed, 2),
            "error_message": None
        }
    except Exception as ex:
        return {
            "sequence": seq,
            "success": False,
            "status_code": 0,
            "request_time_ms": round((time.time() - start) * 1000, 2),
            "error_message": str(ex)
        }

def execute_test_suite(test_run_id: int, db_session_factory):
    db: Session = db_session_factory()
    try:
        test_run = db.query(TestRun).filter(TestRun.id == test_run_id).first()
        if not test_run:
            return

        test_run.status = "RUNNING"
        db.commit()

        results = []
        seq_counter = 1
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=test_run.users) as executor:
            while (time.time() - start_time) < test_run.duration_sec:
                futures = [
                    executor.submit(send_request, test_run.target_url, seq_counter + i)
                    for i in range(test_run.users)
                ]
                seq_counter += test_run.users
                for f in concurrent.futures.as_completed(futures):
                    results.append(f.result())

        # Sort results by sequence order
        results.sort(key=lambda x: x["sequence"])

        success_count = sum(1 for r in results if r["success"])
        failed_count = len(results) - success_count

        # Save results to SQLite
        db_objects = [
            RequestResult(
                test_run_id=test_run_id,
                sequence=r["sequence"],
                request_time_ms=r["request_time_ms"],
                status_code=r["status_code"],
                success=r["success"],
                error_message=r["error_message"]
            )
            for r in results
        ]
        db.bulk_save_objects(db_objects)

        # Save CSV file in exports directory
        export_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "exports"))
        os.makedirs(export_dir, exist_ok=True)
        csv_filename = f"test_run_{test_run_id}.csv"
        csv_path = os.path.join(export_dir, csv_filename)

        df = pd.DataFrame(results)
        df.to_csv(csv_path, index=False)

        # Update TestRun metrics
        test_run.status = "COMPLETED"
        test_run.end_time = datetime.datetime.utcnow()
        test_run.total_requests = len(results)
        test_run.success_count = success_count
        test_run.failed_count = failed_count
        test_run.csv_file_path = csv_path
        db.commit()

    except Exception as e:
        test_run = db.query(TestRun).filter(TestRun.id == test_run_id).first()
        if test_run:
            test_run.status = "FAILED"
            db.commit()
    finally:
        db.close()
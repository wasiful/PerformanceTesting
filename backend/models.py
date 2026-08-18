import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class TestRun(Base):
    __tablename__ = "TestRuns"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    target_url = Column(String(255))
    test_type = Column(String(50))
    users = Column(Integer, default=1)
    duration_sec = Column(Integer, default=10)
    status = Column(String(20), default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    total_requests = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    csv_file_path = Column(String(255), nullable=True)
    
    results = relationship("RequestResult", back_populates="test_run", cascade="all, delete-orphan")

class RequestResult(Base):
    __tablename__ = "RequestResults"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    test_run_id = Column(Integer, ForeignKey("TestRuns.id"))
    sequence = Column(Integer)
    request_time_ms = Column(Float)
    status_code = Column(Integer)
    success = Column(Boolean)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    test_run = relationship("TestRun", back_populates="results")
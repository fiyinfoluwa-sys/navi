from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import random
import json
from typing import List, Optional

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./navi.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Scan model
class ScanDB(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    accessibility_score = Column(Integer)
    ux_ui_score = Column(Integer)
    security_score = Column(Integer)
    issues = Column(JSON)  # Stores issues as JSON
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class ScanRequest(BaseModel):
    url: HttpUrl  # Validates URL format

class ScanResponse(BaseModel):
    id: int
    url: str
    accessibility_score: int
    ux_ui_score: int
    security_score: int
    issues: dict
    timestamp: datetime

    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI(title="Navi SaaS Platform", version="1.0.0")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dummy scan logic (replace with real implementation later)
def perform_scan(url: str) -> dict:
    """Placeholder function for website scanning logic"""
    # Example issues lists
    accessibility_issues = [
        "Missing alt text on images",
        "Low color contrast",
        "Missing form labels",
        "Inaccessible dropdown menus"
    ]
    
    ux_ui_issues = [
        "Button too small on mobile devices",
        "Slow page load time",
        "Inconsistent navigation",
        "Poor readability on small screens"
    ]
    
    security_issues = [
        "Missing HTTPS",
        "Outdated JavaScript libraries",
        "Exposed sensitive information in comments",
        "Vulnerable form endpoints"
    ]

    # Generate random scores
    accessibility_score = random.randint(0, 100)
    ux_ui_score = random.randint(0, 100)
    security_score = random.randint(0, 100)

    # Select random issues based on scores (lower score = more issues)
    num_accessibility_issues = max(1, (100 - accessibility_score) // 25)
    num_ux_ui_issues = max(1, (100 - ux_ui_score) // 25)
    num_security_issues = max(1, (100 - security_score) // 25)

    return {
        "accessibility_score": accessibility_score,
        "ux_ui_score": ux_ui_score,
        "security_score": security_score,
        "issues": {
            "accessibility": random.sample(accessibility_issues, num_accessibility_issues),
            "ux_ui": random.sample(ux_ui_issues, num_ux_ui_issues),
            "security": random.sample(security_issues, num_security_issues)
        }
    }

# API endpoints
@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Navi SaaS Platform",
        "description": "Website accessibility, UX/UI, and security scanning service",
        "version": "1.0.0"
    }

@app.post("/scan", response_model=ScanResponse)
async def scan_website(scan_request: ScanRequest, db: Session = Depends(get_db)):
    """
    Scan a website for accessibility, UX/UI, and security issues
    """
    try:
        # Convert HttpUrl to string for storage
        url_str = str(scan_request.url)
        
        # Perform scan (using dummy data for now)
        scan_results = perform_scan(url_str)
        
        # Create database record
        db_scan = ScanDB(
            url=url_str,
            accessibility_score=scan_results["accessibility_score"],
            ux_ui_score=scan_results["ux_ui_score"],
            security_score=scan_results["security_score"],
            issues=scan_results["issues"]
        )
        
        # Save to database
        db.add(db_scan)
        db.commit()
        db.refresh(db_scan)
        
        return db_scan
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@app.get("/scans", response_model=List[ScanResponse])
async def get_all_scans(db: Session = Depends(get_db)):
    """
    Retrieve all past scans from the database
    """
    try:
        scans = db.query(ScanDB).order_by(ScanDB.timestamp.desc()).all()
        return scans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve scans: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

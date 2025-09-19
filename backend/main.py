from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///./navi.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Incident database model
class IncidentDB(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic model for API
class Incident(BaseModel):
    id: int
    title: str
    description: str
    status: str

app = FastAPI(title="Navi MVP Backend")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Navi MVP Backend!"}

@app.post("/report-incident")
def report_incident(incident: Incident):
    db = next(get_db())
    db_incident = IncidentDB(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return {"message": "Incident reported successfully", "incident": incident}

@app.get("/incidents", response_model=List[Incident])
def get_incidents():
    db = next(get_db())
    incidents = db.query(IncidentDB).all()
    return incidents


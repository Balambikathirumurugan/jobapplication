from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import enum

# -------------------------------
# Database Setup
# -------------------------------

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@localhost/jobstracker"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"charset": "utf8mb4"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -------------------------------
# FastAPI App
# -------------------------------

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Enum and Models
# -------------------------------

class StatusEnum(str, enum.Enum):
    Applied = "Applied"
    Interviewing = "Interviewing"
    Offered = "Offered"
    Rejected = "Rejected"

class JobBase(BaseModel):
    company_name: str
    job_role: str
    status: StatusEnum

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    class Config:
        from_attributes = True  # Pydantic v2 compatibility

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    job_role = Column(String(255), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)

Base.metadata.create_all(bind=engine)

# -------------------------------
# Dependency
# -------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# CRUD Endpoints
# -------------------------------

@app.post("/jobs/", response_model=Job)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = JobModel(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs/", response_model=list[Job])
def read_jobs(db: Session = Depends(get_db)):
    return db.query(JobModel).all()

@app.put("/jobs/{job_id}", response_model=Job)
def update_job(job_id: int, updated_job: JobCreate, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.company_name = updated_job.company_name
    job.job_role = updated_job.job_role
    job.status = updated_job.status
    db.commit()
    db.refresh(job)
    return job

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"detail": "Job deleted successfully"}

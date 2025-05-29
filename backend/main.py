from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector
from sqlalchemy.orm import Session


# Database configuration
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:@localhost/jobstracker"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"charset": "utf8mb4"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# CORS configuration
app = FastAPI()
origins = ["http://localhost:3000"]  # React frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class JobBase(BaseModel):
    company_name: str
    job_role: str
    status: str

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int

    class Config:
        orm_mode = True

# SQLAlchemy model
class JobModel(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    job_role = Column(String)
    status = Column(Enum("Applied", "Interviewing", "Offered", "Rejected", name="status_enum"))

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
@app.post("/jobs/", response_model=Job)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = JobModel(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs/", response_model=list[Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(JobModel).offset(skip).limit(limit).all()
    return jobs

@app.get("/jobs/{job_id}", response_model=Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.put("/jobs/{job_id}", response_model=Job)
def update_job(job_id: int, job: JobCreate, db: Session = Depends(get_db)):
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    for key, value in job.dict().items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.delete("/jobs/{job_id}", response_model=Job)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return db_job

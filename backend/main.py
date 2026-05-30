from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uvicorn

from backend.database import SessionLocal, init_db
from backend.mvp.athletes import Athlete
from backend.mvp.practices import Practice
from backend.auth import get_current_user

app = FastAPI(title="JuniorCoach")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AthleteCreate(BaseModel):
    name: str
    team: str = None
    age: int = None
    position: str = None
    notes: str = None

class PracticeCreate(BaseModel):
    title: str
    date: str
    team: str = None
    duration: int = 60
    location: str = None
    notes: str = None

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "JuniorCoach API is running"}

@app.get("/api/athletes")
def get_athletes(db: Session = Depends(get_db)):
    return db.query(Athlete).all()

@app.post("/api/athletes")
def create_athlete(athlete: AthleteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_athlete = Athlete(**athlete.dict())
    db.add(new_athlete)
    db.commit()
    db.refresh(new_athlete)
    return new_athlete

@app.get("/api/practices")
def get_practices(db: Session = Depends(get_db)):
    return db.query(Practice).all()

@app.post("/api/practices")
def create_practice(practice: PracticeCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_practice = Practice(**practice.dict())
    db.add(new_practice)
    db.commit()
    db.refresh(new_practice)
    return new_practice

@app.get("/api/export/athletes")
def export_athletes(db: Session = Depends(get_db)):
    athletes = db.query(Athlete).all()
    return [{"id": a.id, "name": a.name, "team": a.team, "age": a.age} for a in athletes]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
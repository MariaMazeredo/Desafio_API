from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Athlete(BaseModel):
    id: int
    name: str
    age: int
    category: str

class Score(BaseModel):
    athlete_id: int
    score: int
    event: str

athletes = []
scores = []

@app.post("/athletes/", response_model=Athlete)
async def create_athlete(athlete: Athlete):
    for a in athletes:
        if a.id == athlete.id:
            raise HTTPException(status_code=400, detail="Athlete already exists")
    athletes.append(athlete)
    return athlete

@app.get("/athletes/", response_model=List[Athlete])
async def get_athletes():
    return athletes

@app.post("/scores/", response_model=Score)
async def create_score(score: Score):
    for s in scores:
        if s.athlete_id == score.athlete_id and s.event == score.event:
            raise HTTPException(status_code=400, detail="Score for this event already exists")
    scores.append(score)
    return score

@app.get("/scores/", response_model=List[Score])
async def get_scores():
    return scores

@app.get("/scores/{athlete_id}", response_model=List[Score])
async def get_athlete_scores(athlete_id: int):
    athlete_scores = [score for score in scores if score.athlete_id == athlete_id]
    return athlete_scores
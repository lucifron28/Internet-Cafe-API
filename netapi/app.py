from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Session(BaseModel):
    id: str
    start_time: str  # Time only
    end_time: Optional[str]  # Time only
    status: str
    paid_amount: float

# Sample data
sessions = [
    Session(id="session1", start_time="09:00:00", end_time=None, status="active", paid_amount=10.0),
    Session(id="session2", start_time="10:00:00", end_time="11:00:00", status="completed", paid_amount=15.0),
    Session(id="session3", start_time="11:00:00", end_time=None, status="active", paid_amount=20.0),
    Session(id="session4", start_time="12:00:00", end_time=None, status="active", paid_amount=25.0),
    Session(id="session5", start_time="13:00:00", end_time=None, status="active", paid_amount=30.0)
]

# CRUD endpoints for Sessions
@app.post("/sessions/", response_model=Session)
def create_session(session: Session):
    sessions.append(session)
    return session

@app.get("/sessions/", response_model=List[Session])
def get_sessions():
    return sessions

@app.get("/sessions/{session_id}", response_model=Session)
def get_session(session_id: str):
    session = next((session for session in sessions if session.id == session_id), None)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.put("/sessions/{session_id}", response_model=Session)
def update_session(session_id: str, updated_session: Session):
    for index, session in enumerate(sessions):
        if session.id == session_id:
            sessions[index] = updated_session
            return updated_session
    raise HTTPException(status_code=404, detail="Session not found")

@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    global sessions
    sessions = [session for session in sessions if session.id != session_id]
    return {"message": "Session deleted"}
from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from app.services.game_logic import GameLogic
from app.ml.classifier import classify_image
from sqlalchemy.orm import Session
from app.core import models
from app.core.config import get_db
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Existing routes
@router.post("/start-game")
async def start_game(player1_id: str, player2_id: str, session_id: str):
    GameLogic.start_game(session_id, player1_id, player2_id)
    return {"status": "Game started", "session_id": session_id}

@router.post("/submit-drawing")
async def submit_drawing(
    session_id: str,
    player_id: str,
    file: UploadFile
):
    # Classify the drawing
    label, confidence = classify_image(file.file)
    
    # Submit the drawing for the current game session
    result = GameLogic.submit_drawing(session_id, player_id, label, confidence)
    return result

@router.get("/get-level/{player_id}")
async def get_level(player_id: str):
    return GameLogic.get_player_level(player_id)

@router.post("/matchmake")
async def matchmake(player_id: str, player_xp: int):
    result = GameLogic.matchmake(player_id, player_xp)
    return result

# New routes for handling players and game sessions

# Pydantic schemas for validation and serialization

class PlayerCreate(BaseModel):
    name: str
    xp: Optional[int] = 0

class PlayerResponse(BaseModel):
    id: int
    name: str
    xp: int

    class Config:
        orm_mode = True

class GameSessionCreate(BaseModel):
    player1_id: int
    player2_id: int
    round_number: Optional[int] = 1
    winner_id: Optional[int] = None

class GameSessionResponse(BaseModel):
    id: int
    player1_id: int
    player2_id: int
    round_number: int
    winner_id: Optional[int] = None

    class Config:
        orm_mode = True

# Create a new player
@router.post("/players/", response_model=PlayerResponse)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_player = db.query(models.Player).filter(models.Player.name == player.name).first()
    if db_player:
        raise HTTPException(status_code=400, detail="Player already registered")
    
    new_player = models.Player(name=player.name, xp=player.xp)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

# Get a list of all players
@router.get("/players/", response_model=List[PlayerResponse])
def get_players(db: Session = Depends(get_db)):
    return db.query(models.Player).all()

# Get a single player by ID
@router.get("/players/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

# Create a new game session
@router.post("/game_sessions/", response_model=GameSessionResponse)
def create_game_session(game_session: GameSessionCreate, db: Session = Depends(get_db)):
    db_player1 = db.query(models.Player).filter(models.Player.id == game_session.player1_id).first()
    db_player2 = db.query(models.Player).filter(models.Player.id == game_session.player2_id).first()
    
    if not db_player1 or not db_player2:
        raise HTTPException(status_code=400, detail="Both players must exist")

    new_game_session = models.GameSession(
        player1_id=game_session.player1_id,
        player2_id=game_session.player2_id,
        round_number=game_session.round_number,
        winner_id=game_session.winner_id
    )
    
    db.add(new_game_session)
    db.commit()
    db.refresh(new_game_session)
    return new_game_session

# Get a list of all game sessions
@router.get("/game_sessions/", response_model=List[GameSessionResponse])
def get_game_sessions(db: Session = Depends(get_db)):
    return db.query(models.GameSession).all()

# Get a game session by ID
@router.get("/game_sessions/{game_session_id}", response_model=GameSessionResponse)
def get_game_session(game_session_id: int, db: Session = Depends(get_db)):
    db_game_session = db.query(models.GameSession).filter(models.GameSession.id == game_session_id).first()
    if db_game_session is None:
        raise HTTPException(status_code=404, detail="Game session not found")
    return db_game_session

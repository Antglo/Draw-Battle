from fastapi import APIRouter, UploadFile, Form
from app.services.game_logic import GameLogic
from app.ml.classifier import classify_image

router = APIRouter()

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

@router.get("/get-level/{player_id}")
async def get_level(player_id: str):
    return GameLogic.get_player_level(player_id)

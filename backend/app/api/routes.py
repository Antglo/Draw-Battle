# backend/app/api/routes.py

from fastapi import APIRouter, UploadFile, Form
from app.ml.classifier import classify_image
from app.services.game_logic import SessionManager, determine_winner

router = APIRouter()
session_manager = SessionManager()

@router.post("/upload-drawing")
async def upload_drawing(
    file: UploadFile,
    session_id: str = Form(...),
    player_id: str = Form(...)
):
    # Read uploaded image
    image_bytes = await file.read()

    # Classify image to get label
    drawing_label = classify_image(image_bytes)

    # Add the label to the session
    session_manager.add_player_drawing(session_id, player_id, drawing_label)

    # Check session for both players
    session_data = session_manager.get_session_data(session_id)
    if len(session_data) == 2:
        # Process game logic if both players have submitted
        player_ids = list(session_data.keys())
        labels = list(session_data.values())
        result = determine_winner(labels[0], labels[1])

        # Clear session after determining the result
        session_manager.clear_session(session_id)

        return {"result": result, "details": session_data}

    return {"status": "Waiting for the other player", "current_data": session_data}

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a TestClient instance for FastAPI
client = TestClient(app)

def test_start_game():
    response = client.post(
        "/start-game", 
        params={"player1_id": "player1", "player2_id": "player2", "session_id": "session123"}
    )
    assert response.status_code == 200
    assert response.json() == {"status": "Game started", "session_id": "session123"}

def test_submit_drawing():
    with open("test_image.jpg", "rb") as img:
        response = client.post(
            "/submit-drawing", 
            params={"session_id": "session123", "player_id": "player1"},
            files={"file": ("test_image.jpg", img, "image/jpeg")}
        )
    assert response.status_code == 200
    # Adjust the response assert based on your actual implementation
    assert "result" in response.json()

def test_get_level():
    response = client.get("/get-level/player1")
    assert response.status_code == 200
    # Add a more specific assertion based on your implementation
    assert "level" in response.json()

def test_matchmake():
    response = client.post("/matchmake", params={"player_id": "player1", "player_xp": 100})
    assert response.status_code == 200
    # Adjust the response assert based on your actual implementation
    assert "match" in response.json()

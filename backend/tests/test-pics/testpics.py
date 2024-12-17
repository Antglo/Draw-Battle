import requests

url = "http://127.0.0.1:8000/upload-drawing"

# Player 1 Submission
response1 = requests.post(
    url,
    files={"file": open("/home/ubuntu/Draw-Battle/backend/tests/test-pics/shield.png", "rb")},
    data={"session_id": "game1234", "player_id": "player1"}
)
print(response1.json())

# Player 2 Submission
response2 = requests.post(
    url,
    files={"file": open("/home/ubuntu/Draw-Battle/backend/tests/test-pics/sword.png", "rb")},
    data={"session_id": "game1234", "player_id": "player2"}
)
print(response2.json())

import random

class GameLogic:
    sessions = {}
    matchmaking_queue = []  # Queue for players waiting for a game

    @classmethod
    def start_game(cls, session_id, player1_id, player2_id):
        """Initialize a new game with 3 rounds."""
        cls.sessions[session_id] = {
            "player1": {"id": player1_id, "xp": 0, "drawings": []},
            "player2": {"id": player2_id, "xp": 0, "drawings": []},
            "rounds": 3,  # 3 rounds per game
            "current_round": 1,
            "winner": None
        }

    @classmethod
    def submit_drawing(cls, session_id, player_id, drawing_label, confidence):
        """Submit a drawing for a player and evaluate the round."""
        game_session = cls.sessions.get(session_id)
        if not game_session:
            return {"error": "Game session not found"}

        player = game_session.get(player_id)
        if not player:
            return {"error": "Player not found"}

        # Add the drawing and confidence to the player's submission list
        player["drawings"].append((drawing_label, confidence))

        # Check if both players have submitted their drawing for the current round
        if len(game_session["player1"]["drawings"]) == game_session["current_round"] and len(game_session["player2"]["drawings"]) == game_session["current_round"]:
            # Compare the drawings for the round
            player1_confidence = game_session["player1"]["drawings"][-1][1]
            player2_confidence = game_session["player2"]["drawings"][-1][1]

            winner = "player1" if player1_confidence > player2_confidence else "player2"
            game_session[winner]["xp"] += 10  # Reward winner with XP

            # Check if all rounds are completed
            if game_session["current_round"] == game_session["rounds"]:
                game_session["winner"] = winner
                return {"result": f"{winner} wins the game", "player1_xp": game_session["player1"]["xp"], "player2_xp": game_session["player2"]["xp"]}

            # Move to the next round
            game_session["current_round"] += 1
            return {"status": f"Round {game_session['current_round']} ongoing", "player1_xp": game_session["player1"]["xp"], "player2_xp": game_session["player2"]["xp"]}

        return {"status": f"Waiting for drawings for round {game_session['current_round']}", "player1_xp": game_session["player1"]["xp"], "player2_xp": game_session["player2"]["xp"]}

    @classmethod
    def get_player_level(cls, player_id):
        """Return the player's level based on XP."""
        # Leveling up logic: The more XP, the higher the level
        player = next(p for s in cls.sessions.values() for p in s.values() if p["id"] == player_id)
        xp = player["xp"]
        level = xp // 100  # Example: Every 100 XP gets a new level
        return {"player_id": player_id, "xp": xp, "level": level}

    @classmethod
    def matchmake(cls, player_id, player_xp):
        """Matchmake the player with someone of similar XP."""
        player = {"id": player_id, "xp": player_xp}
        cls.matchmaking_queue.append(player)

        # Try to find a match within a specific XP tolerance (e.g., +/- 10 XP)
        potential_opponent = None
        for queued_player in cls.matchmaking_queue:
            if abs(queued_player["xp"] - player_xp) <= 10:  # 10 XP tolerance for matchmaking
                potential_opponent = queued_player
                break

        if potential_opponent:
            # Remove both players from the queue
            cls.matchmaking_queue.remove(player)
            cls.matchmaking_queue.remove(potential_opponent)

            # Start a new game session
            session_id = f"game_{random.randint(1000, 9999)}"
            cls.start_game(session_id, player_id, potential_opponent["id"])
            return {"status": "Game started", "session_id": session_id, "player1": player_id, "player2": potential_opponent["id"]}

        return {"status": "Waiting for opponent"}
    
    @classmethod
    def reward_xp(cls, session_id):
        """Award XP to the winner and update player levels."""
        game_session = cls.sessions.get(session_id)
        if not game_session:
            return {"error": "Game session not found"}

        winner = game_session["winner"]
        if winner:
            # Award XP to the winner
            game_session[winner]["xp"] += 10

            # Calculate new level
            winner_level = game_session[winner]["xp"] // 100  # Level up every 100 XP

            # Return result with XP and level information
            return {"status": f"{winner} wins the game!", "winner_xp": game_session[winner]["xp"], "winner_level": winner_level}

        return {"status": "Game has no winner"}

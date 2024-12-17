# backend/app/services/game_logic.py

class SessionManager:
    def __init__(self):
        # Temporary in-memory session store
        self.sessions = {}

    def add_player_drawing(self, session_id: str, player_id: str, drawing_label: str):
        """
        Adds a player's drawing label to a session.
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = {}

        self.sessions[session_id][player_id] = drawing_label

    def get_session_data(self, session_id: str) -> dict:
        """
        Retrieves session data for a specific session ID.
        """
        return self.sessions.get(session_id, {})

    def clear_session(self, session_id: str):
        """
        Clears session data after processing.
        """
        if session_id in self.sessions:
            del self.sessions[session_id]


def determine_winner(player1: str, player2: str) -> str:
    """
    Determines the winner based on predefined game rules.
    """
    # Rules for deciding the winner
    rules = {
        "sword": ["shield", "arrow"],
        "shield": ["arrow"],
        "arrow": ["sword"],
    }

    if player2 in rules.get(player1, []):
        return "Player 1 wins"
    elif player1 in rules.get(player2, []):
        return "Player 2 wins"
    else:
        return "It's a draw"

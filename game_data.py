import json
import os
from datetime import datetime


class GameData:
    def __init__(self, filename="data/game_sessions.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.sessions = self.load_sessions()

    def load_sessions(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_session(self, player_name, score, game_time, asteroids_destroyed):
        session = {
            "player_name": player_name,
            "score": score,
            "game_duration": round(game_time, 2),
            "timestamp": datetime.now().isoformat(),
            "asteroids_destroyed": asteroids_destroyed
        }
        self.sessions.append(session)

        with open(self.filename, 'w') as f:
            json.dump(self.sessions, f, indent=2)

    def get_highscore(self):
        if not self.sessions:
            return 0
        return max(session['score'] for session in self.sessions)

    def get_highscore_player(self):
        if not self.sessions:
            return None
        best_session = max(self.sessions, key=lambda x: x['score'])
        return best_session['player_name']

    def get_top_players(self, limit=5):
        if not self.sessions:
            return []
        sorted_sessions = sorted(self.sessions, key=lambda x: x['score'], reverse=True)
        return sorted_sessions[:limit]

"""Module de match facilitant la lecture des matchs de l'API NBA"""

import requests

from core.date import GameDateTime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.nba.com/",
}


def fetch_game(game_id: str) -> dict:
    """
    Récupère les données live d'un match spécifique via son game_id.
    """
    url = f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game_id}.json"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        raise ConnectionError(f"Impossible de récupérer le match {game_id} : {e}")


class match:
    def __init__(self, match_data: dict):
        self.base_data = match_data
        self._homeTeam = match_data["homeTeam"]
        self._awayTeam = match_data["awayTeam"]
        self._arena = match_data["arenaName"]
        self._game_status = match_data["gameStatus"]
        self._week_number = match_data["weekNumber"]
        self._tricodes = {
            "homeTeam": match_data["homeTeam"]["teamTricode"],
            "awayTeam": match_data["awayTeam"]["teamTricode"],
        }
        self._game_date = GameDateTime.from_iso_utc(match_data["gameDateTimeUTC"])
        self._match_data = None

    @property
    def game_status(self):
        """Renvoie le statue du match
        1 : Match à venir
        2 : Match en cours
        3 : Match fini
        """
        return self._game_status

    @property
    def arena(self):
        return self._arena

    @property
    def week_number(self):
        """Renvoie le numéro de semaine du match"""
        return self._week_number

    @property
    def teams_tricode(self):
        """Renvoie les tricodes des 2 équipes
        return dict{'homeTeam':homeTeamTricode, 'awayTeam':awayTeamTricode}
        """
        return self._tricodes

    @property
    def homeTeam(self):
        """Renvoie les states de la partie de l'équipe à domicile"""
        return self._homeTeam

    @property
    def awayTeam(self):
        """Renvoie les states de la partie de l'équipe à l'extérieur"""
        return self._awayTeam

    @property
    def game_date(self):
        """Renvoie la date en heure française du match"""
        return self._game_date

    def get_points_leaders(self):
        """Renvoie le/les leader(s) en nombre de points"""
        return self.base_data["pointsLeaders"]

    def load_match_data(self):
        """Récupère les données de la partie en ligne"""
        self._match_data = fetch_game(game_id=self.base_data["gameId"])["game"]

    def __repr__(self):
        return f"Match <{self._tricodes['homeTeam']},{self._tricodes['awayTeam']}> ({str(self._game_date)})"

    def __str__(self):
        return f"Match {self._tricodes['awayTeam']} @ {self._tricodes['homeTeam']} - {str(self._game_date)}"

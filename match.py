"""Module de match facilitant la lecture des matchs de l'API NBA"""

from date import GameDateTime

class match:

    def __init__(self, match_data:dict):
        self.raw_data = match_data
        self._homeTeam = match_data['homeTeam']
        self._awayTeam = match_data['awayTeam']
        self._game_status = match_data['gameStatus']
        self._week_number = match_data['weekNumber']
        self._tricodes = {'homeTeam':match_data['homeTeam']['teamTricode'], 'awayTeam':match_data['awayTeam']['teamTricode']}
        self._game_date = GameDateTime.from_iso_utc(match_data['gameDateTimeUTC'])

    @property
    def game_status(self):
        """Renvoie le statue du match
            1 : Match à venir
            2 : Match en cours
            3 : Match fini
        """
        return self._game_status

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
        return self._homeTeam

    @property
    def awayTeam(self):
        return self._awayTeam

    @property
    def game_date(self):
        """Renvoie la date en heure française du match"""
        return self._game_date

    def __repr__(self):
        return f"Match <{self._tricodes['homeTeam']},{self._tricodes['awayTeam']}> ({str(self._game_date)})"
    
    def __str__(self):
        return f"Match {self._tricodes['awayTeam']} @ {self._tricodes['homeTeam']} - {str(self._game_date)}"
"""Module facilitant la lecture des données de toute la league"""

# Module interne
from core._team_data import NBA_TEAMS, Conference
from core.TeamData import TeamData
from core.utils import classer_dictionnaire


class LeagueData:
    """LeagueData permet d'obtenir tout les infos et statistique sur la NBA"""

    def __init__(self):
        self._teams: dict = {key: TeamData(key) for key in NBA_TEAMS.keys()}
        self._east_teams = {
            key: TeamData(key)
            for key in NBA_TEAMS.keys()
            if NBA_TEAMS[key].conference == Conference.EAST
        }
        self._west_teams = {
            key: TeamData(key)
            for key in NBA_TEAMS.keys()
            if NBA_TEAMS[key].conference == Conference.WEST
        }

    @property
    def teams(self):
        """Renvoie un dictionnaire contenant toutes les équipes de NBA
        return {tricode (str): team (TeamData)}
        """
        return self._teams

    def get_team(self, tricode: str) -> TeamData:
        """Renvoie la TeamData associé au tricode de l'équipe"""
        return self._teams[tricode]

    @property
    def east_conference_teams(self):
        """Renvoie les équipes de la conférence Est"""
        return self._east_teams

    @property
    def west_conference_teams(self):
        """Renvoie les équipes de la conférence Ouest"""
        return self._west_teams

    def get_classement(self):
        """Renvoie le classement total sous forme de dictionnaire, le classement dépend du winrate de l'équipe
        return Dict{position (int):team (TeamData)}
        """
        return classer_dictionnaire(self.teams, TeamData.get_winrate)

    def get_classement_east(self):
        """Renvoie le classement de la conférence est sous forme de dictionnaire,
        le classement dépend du winrate de l'équipe
            return Dict{position (int):team (TeamData)}
        """
        return classer_dictionnaire(self.east_conference_teams, TeamData.get_winrate)

    def get_classement_west(self):
        """Renvoie le classement de la conférence ouest sous forme de dictionnaire,
        le classement dépend du winrate de l'équipe
            return Dict{position (int):team (TeamData)}
        """
        return classer_dictionnaire(self.west_conference_teams, TeamData.get_winrate)

#!/usr/bin/env python3
"""Module proposant la classe inf_team"""

from utils import est_valide_3C,fetch_schedule
from _team_data import NBA_TEAMS

class TeamNonExistanteErreur(Exception):
    pass


class info_team:
    """Team permet d'obtenir tout les infos et statistique sur une équipe NBA

        arguments: 
        team_3C -- String de 3 charactère identifiant une équipe (e.g: NYK, SAS,...)
    qui permet d'itentifier correctement la team NBA voulu
    """

    def __init__(self, team_3C:str) -> None:
        if est_valide_3C(team_3C):
            raise TeamNonExistanteErreur(f"L'équipe {team_3C} n'existe pas")
        self._team = NBA_TEAMS[team_3C]

    def __str__(self):
        return str(self._team)

    @property
    def team(self):
        return self._team
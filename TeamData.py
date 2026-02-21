#!/usr/bin/env python3
"""Module proposant la classe inf_team"""

from schedule import Schedule
from _team_data import NBA_TEAMS
from utils import est_valide_tricode

class TeamNonExistanteErreur(Exception):
    pass


class TeamData:
    """Team permet d'obtenir tout les infos et statistique sur une équipe NBA

        arguments: 
        team_tricode -- String de 3 charactère identifiant une équipe (e.g: NYK, SAS,...)
    qui permet d'itentifier correctement la team NBA voulu
    """

    _schedule = Schedule()

    def __init__(self, team_tricode:str) -> None:
        if not est_valide_tricode(team_tricode):
            raise TeamNonExistanteErreur(f"L'équipe {team_tricode} n'existe pas")
        self._team = NBA_TEAMS[team_tricode]
        self._team_schedule = Schedule(gamesData=TeamData._schedule.get_matchs_x_team(team_tricode))

    def get_all_matchs(self):
        """Renvoie le planning complet de la team """
        return self._team_schedule.get_all_matchs()

    def get_all_coming_matchs(self):
        """Renvoie les matchs à venir de la team """
        return self._team_schedule.get_all_coming_matchs()

    def get_all_finished_matchs(self):
        """Renvoie les matchs finie de la team """
        return self._team_schedule.get_all_finished_matchs()
    
    def get_next_match(self):
        """Renvoie le prochain match de la team """
        return self._team_schedule.get_all_coming_matchs()[0]

    def get_all_matchup(self,matchup_tricode:str):
        """Renvoie la liste complète des matchs entre la team et son matchup"""
        if not est_valide_tricode(matchup_tricode):
            raise TeamNonExistanteErreur(f"L'équipe {matchup_tricode} n'existe pas")
        return self._team_schedule.get_matchs_x_team(matchup_tricode)

    def __str__(self):
        return str(self._team)

    @property
    def team(self):
        return self._team
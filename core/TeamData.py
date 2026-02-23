#!/usr/bin/env python3
"""Module proposant la classe inf_team"""

from core.schedule import Schedule
from core._team_data import NBA_TEAMS
from core.utils import est_valide_tricode

class TeamNonExistanteErreur(Exception):
    pass

class TeamData:
    """TeamData permet d'obtenir tout les infos et statistique sur une équipe NBA

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
        self._W = int(self.get_win_lose()['win'])
        self._L = int(self.get_win_lose()['lose'])

    @property
    def schedule(self):
        return self._schedule

    @property    
    def tricode(self):
        return self._team.tricode 
    
    @property    
    def W(self):
        return self._W 
    
    @property    
    def L(self):
        return self._L
    
    def get_all_matchs(self) -> list:
        """Renvoie le planning complet de la team """
        return self.schedule.get_all_matchs()

    def get_all_coming_matchs(self) -> list:
        """Renvoie les matchs à venir de la team """
        return self.schedule.get_all_coming_matchs()

    def get_all_finished_matchs(self) -> list:
        """Renvoie les matchs finie de la team """
        return self.schedule.get_all_finished_matchs()
    
    def get_last_match(self):
        """Renvoie le dernier match joué de l'équipe"""
        return self.get_all_finished_matchs()[-1]

    def get_next_match(self):
        """Renvoie le prochain match de la team"""
        return self.schedule.get_all_coming_matchs()[0]

    def get_all_matchup(self,matchup_tricode:str):
        """Renvoie la liste complète des matchs entre la team et son matchup"""
        if not est_valide_tricode(matchup_tricode):
            raise TeamNonExistanteErreur(f"L'équipe {matchup_tricode} n'existe pas")
        return self.schedule.get_matchs_x_team(matchup_tricode)

    def get_win_lose(self):
        """Renvoie un dictionnaire contenant le nombre de victoires et de défaite de l'équipe"""
        last_match = self.get_all_finished_matchs()[-1]
        team_result = last_match.homeTeam if last_match.homeTeam["teamTricode"] == self.tricode else last_match.awayTeam
        return {'win':team_result["wins"],'lose':team_result["losses"]}

    def get_winrate(self):
        """Renvoie le winrate de l'équipe"""
        if self.L == 0:
            return self.W
        return self.W/(self.W + self.L)

    def is_playing_today(self) -> bool:
        """Renvoie si l'équipe joue aujourd'hui"""
        return self.get_next_match().game_date.is_today_us()

    def __str__(self):
        return f"{str(self._team)} - {self.W}W | {self.L}L"
    
    def __repr__(self):
        return f"TeamData<{str(self._team)}>"

    @property
    def team(self):
        return self._team
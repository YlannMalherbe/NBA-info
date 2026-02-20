#!/usr/bin/env python3
"""Module proposant la classe schedule"""

import requests
from utils import est_valide_3C
from date import GameDateTime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.nba.com/",
}

def fetch_schedule() -> dict:
    """Renvoie le json contenant les informations et le planning des matches"""
    url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()


class schedule:
    """
        Classe Schedule permetant de gérer facilement le planning NBA et acceder rapidement au information
    """

    def __init__(self):
        self._data = fetch_schedule()
        self._leagueSchedule = self._data['leagueSchedule']
        self._weeks = self._leagueSchedule['weeks']
        self._games = self._leagueSchedule['gameDates']
        self._clean = False 
        self.today = GameDateTime.now()

    def clean(self):
        return self._clean

    def getYear(self) -> "datetime":
        """Renvoie l'année de la saison actuelle de NBA """
        return leagueSchedule['seasonYear']

    def get_all_matchs(self) -> list:
        """Renvoie tous les matchs de la saison (final de playoffs inclue)"""
        if not self.clean():
            games = []
            for jour in self._games:
                for game in jour['games']:
                    games.append(game)
            self._games = games
            self._clean = True
        return self._games
    
    def get_all_finished_matchs(self):
        """Renvoie les matchs finie de la saison (final de playoffs inclue)"""
        matchs = self.get_all_matchs()
        res = []
        for match in matchs:
            if match['gameStatus'] == 3:
                res.append(match)
        return res

    def get_all_coming_matchs(self):
        """Renvoie les matchs a venir de la saison (final de playoffs inclue)"""
        matchs = self.get_all_matchs()
        res = []
        for match in matchs:
            if match['gameStatus'] == 1:
                res.append(match)
        return res

    def get_matchs_x_weeks(self, x:int):
        """Renvoie les matchs de la x_ième semaine de la saison (final de playoffs inclue)"""
        ...

    def get_matchs_today(self):
        """Renvoie les matchs du jour"""
        ...
    
    def get_all_current_matchs(self):
        """Renvoie les matchs en cours"""
        matchs = self.get_all_matchs()
        res = []
        for match in matchs:
            if match['gameStatus'] == 2:
                res.append(match)
        return res
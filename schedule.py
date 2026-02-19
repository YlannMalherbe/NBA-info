#!/usr/bin/env python3
"""Module proposant la classe schedule"""

import requests
from utils import est_valide_3C

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
        data = fetch_schedule()
        leagueSchedule = data['leagueSchedule']
        weeks = leagueSchedule['weeks']
        games = leagueSchedule['gameDates']


    def getYear(self):
        """Renvoie l'année de la saison actuelle de NBA """
        return leagueSchedule['seasonYear']
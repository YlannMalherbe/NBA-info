#!/usr/bin/env python3
"""Module proposant la classe schedule"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import requests

from core.date import GameDateTime
from core.match import match

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.nba.com/",
}

CACHE_DURATION = timedelta(hours=6)

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
CACHE_FILE = ASSETS_DIR / "schedule_cache.json"


class ConnectionFailedError(Exception):
    pass


def _save_cache(data: dict):
    """Fonction pour faire un cache des données de l'API NBA"""
    cache_content = {"last_update": datetime.utcnow().isoformat(), "data": data}
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_content, f, ensure_ascii=False, indent=4)


def _load_cache():
    """Fonction pour récuperer le cache enregistré de l'API"""
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _is_cache_valid(cache: dict) -> bool:
    """Fonction pour vérifier si le cache à besoin d'être update ou non"""
    last_update = datetime.fromisoformat(cache["last_update"])
    return datetime.utcnow() - last_update < CACHE_DURATION


def fetch_schedule(force_refresh: bool = False) -> dict:
    """
    Récupère le schedule NBA.

    - Si cache valide → retourne cache
    - Si cache expiré → tente refresh
    - Si refresh échoue → fallback sur ancien cache
    - Si aucun cache dispo → erreur
    """
    if os.path.exists(CACHE_FILE) and not force_refresh:
        cache = _load_cache()
        if _is_cache_valid(cache):
            return cache["data"]
    try:
        url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()
        if not data:
            raise ConnectionFailedError("Réponse vide reçue depuis l'API NBA.")
        _save_cache(data)
        return data
    except (requests.RequestException, ConnectionFailedError) as e:
        if os.path.exists(CACHE_FILE):
            return _load_cache()["data"]
        raise ConnectionFailedError(
            "Impossible de récupérer les données NBA et aucun cache disponible."
        )


class Schedule:
    """
    Classe Schedule permetant de gérer facilement le planning NBA et acceder rapidement au information

    Une liste de match peut être fourni à l'initialisation pour généraliser l'utilisation de schedule
    """

    def __init__(self, gamesData=None):
        if gamesData == None:
            self._data = fetch_schedule()
            self._games = self._data["leagueSchedule"]["gameDates"]
        else:
            self._games = gamesData
        self._clean = gamesData != None
        self.today = GameDateTime.now()

    def clean(self):
        """Renvoie est-ce que les données on été traité ou non"""
        return self._clean

    def get_all_matchs(self) -> list:
        """Renvoie tous les matchs de la saison (final de playoffs inclue)"""
        if not self.clean():
            games = []
            for jour in self._games:
                for game in jour["games"]:
                    games.append(match(game))
            self._games = games
            self._clean = True
        return self._games

    def get_all_finished_matchs(self):
        """Renvoie les matchs finie de la saison (final de playoffs inclue)"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if game.game_status == 3:
                res.append(game)
        return res

    def get_all_coming_matchs(self):
        """Renvoie les matchs a venir de la saison (final de playoffs inclue)"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if game.game_status == 1:
                res.append(game)
        return res

    def get_matchs_x_weeks(self, x: int):
        """Renvoie les matchs de la x_ième semaine de la saison (final de playoffs inclue)"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if game.week_number == x:
                res.append(game)
        return res

    def get_matchs_x_team(self, tricode: str):
        """Récupère les matchs ou l'équipe x est présente"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if tricode in game.teams_tricode.values():
                res.append(game)
        return res

    def get_matchs_today(self):
        """Renvoie les matchs du jour"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if game.game_date.is_today_us():
                res.append(game)
        return res

    def get_all_current_matchs(self):
        """Renvoie les matchs en cours"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if game.game_status == 2:
                res.append(game)
        return res

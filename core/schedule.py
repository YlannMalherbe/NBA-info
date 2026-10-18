#!/usr/bin/env python3
"""Module proposant la classe schedule"""

import json
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import requests

from core.date import GameDateTime
from core.match import match
from core.nba_http import HEADERS

CACHE_DURATION = timedelta(hours=6)

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
CACHE_FILE = ASSETS_DIR / "schedule_cache.json"


class ConnectionFailedError(Exception):
    pass


def _save_cache(data: dict):
    """Fonction pour faire un cache des données de l'API NBA"""
    cache_content = {"last_update": datetime.utcnow().isoformat(), "data": data}
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=ASSETS_DIR, delete=False
        ) as f:
            temporary_path = Path(f.name)
            json.dump(cache_content, f, ensure_ascii=False, indent=4)
        os.replace(temporary_path, CACHE_FILE)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def _load_cache():
    """Fonction pour récuperer le cache enregistré de l'API"""
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        _is_cache_valid(cache)
        if not isinstance(cache["data"]["leagueSchedule"]["gameDates"], list):
            return None
        return cache
    except (OSError, ValueError, KeyError, TypeError):
        return None


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
    cache = _load_cache()
    if cache is not None and not force_refresh and _is_cache_valid(cache):
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
    except (requests.RequestException, ConnectionFailedError):
        if cache is not None:
            return cache["data"]
        raise ConnectionFailedError(
            "Impossible de récupérer les données NBA et aucun cache disponible."
        )


class Schedule:
    """
    Classe Schedule permetant de gérer facilement le planning NBA et acceder rapidement au information

    Une liste de match peut être fourni à l'initialisation pour généraliser l'utilisation de schedule
    """

    def __init__(self, gamesData=None):
        if gamesData is None:
            self._data = fetch_schedule()
            self._games = self._data["leagueSchedule"]["gameDates"]
        else:
            self._games = gamesData
        self._clean = gamesData is not None
        self.today = GameDateTime.now()

    def clean(self) -> bool:
        """Renvoie est-ce que les données on été traité ou non"""
        return self._clean

    def get_all_matchs(self) -> list[match]:
        """Renvoie tous les matchs de la saison (final de playoffs inclue)"""
        if not self.clean():
            games = []
            for jour in self._games:
                for game in jour["games"]:
                    games.append(match(game))
            self._games = games
            self._clean = True
        return self._games

    def get_all_finished_matchs(self) -> list[match]:
        """Renvoie les matchs finie de la saison (final de playoffs inclue)"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if game.game_status == 3:
                res.append(game)
        return res

    def get_all_coming_matchs(self) -> list[match]:
        """Renvoie les matchs a venir de la saison (final de playoffs inclue)"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if game.game_status == 1:
                res.append(game)
        return res

    def get_matchs_x_weeks(self, x: int) -> list[match]:
        """Renvoie les matchs de la x_ième semaine de la saison (final de playoffs inclue)"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if game.week_number == x:
                res.append(game)
        return res

    def get_matchs_x_team(self, tricode: str) -> list[match]:
        """Récupère les matchs ou l'équipe x est présente"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if tricode in game.teams_tricode.values():
                res.append(game)
        return res

    def get_matchs_today(self) -> list[match]:
        """Renvoie les matchs du jour"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if game.game_date.is_today_us():
                res.append(game)
        return res

    def get_all_current_matchs(self) -> list[match]:
        """Renvoie les matchs en cours"""
        matchs = self.get_all_matchs()
        res = []
        for game in matchs:
            if game.game_status == 2:
                res.append(game)
        return res

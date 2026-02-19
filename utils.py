#!/usr/bin/env python3
"""Module utilitaire """

from _team_data import NBA_TEAMS

def est_valide_3C(team: str) -> bool:
    return team in NBA_TEAMS.keys()

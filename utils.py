"""Module utilitaire pour le projet """

from _team_data import NBA_TEAMS

def est_valide_tricode(team: str) -> bool:
    """Verifie qu'un tricode correspond bien à une équipe NBA valide"""
    return team in NBA_TEAMS.keys()

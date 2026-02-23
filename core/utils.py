"""Module utilitaire pour le projet """

from core._team_data import NBA_TEAMS

def est_valide_tricode(team: str) -> bool:
    """Verifie qu'un tricode correspond bien à une équipe NBA valide"""
    return team in NBA_TEAMS.keys()

def classer_dictionnaire(dico:dict,fct, croissant=False) -> dict:
    """Tri un dictionnaire par rapport à une fonction"""
    res = list(dico.values())
    res.sort(key=fct, reverse= not croissant)
    return {i+1: res[i] for i in range(0,len(res))}
from InquirerPy import inquirer

from core._team_data import NBA_TEAMS


def select_team_menu() -> str:
    return inquirer.select(
        message="Choisis une équipe :",
        choices=NBA_TEAMS.keys(),
    ).execute()

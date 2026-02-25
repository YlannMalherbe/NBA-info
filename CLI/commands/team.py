from typing import Optional

import typer

from CLI.UI.menus import select_team_menu
from CLI.UI.pages import display_info_team
from core.TeamData import TeamData

app = typer.Typer()


@app.command()
def info(
    name: Optional[str] = typer.Argument(
        None, help="Team abbreviation (ex: SAS, DEN, BOS)"
    ),
):
    """
    Display information about an NBA team.
    """

    # 🔹 Mode interactif si aucun argument
    if name is None:
        name = select_team_menu()

    name = name.upper()

    try:
        team_data = TeamData(name)
    except Exception as e:
        typer.echo(f"Erreur lors du chargement de l'équipe : {e}")
        raise typer.Exit(code=1)

    display_info_team(team_data)

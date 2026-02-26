import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from core.league import LeagueData
from core.TeamData import TeamData

console = Console()
app = typer.Typer(help="Afficher le classement NBA")


def format_team_position_row(position: int, team: TeamData):
    """
    Retourne le nom + stats formatés
    """
    name = f"[bold]{position}. {team.team.full_name}"
    stats = f"{team.W}W-{team.L}L ({team.get_winrate() * 100:.1f}%)"
    return name, stats


def create_conference_panel(teams_dict, title: str, color: str) -> Panel:
    """
    Crée un panel pour une conférence avec une seule colonne par équipe
    """
    table = Table.grid(expand=True)
    table.add_column(justify="left")
    table.add_column(justify="right")

    for pos, team in teams_dict.items():
        name, stats = format_team_position_row(pos, team)
        table.add_row(name, stats)
        if pos == 6:
            table.add_row("[yellow]------ Playoffs ------", "[yellow]---------------")

        if pos == 10:
            table.add_row("[red]------ Play-in ------", "[red]---------------")

    return Panel(table, title=title, border_style=color, expand=True)


@app.command()
def classement():
    """
    Affiche le classement NBA Est / Ouest côte à côte dans un panel global.
    """
    league = LeagueData()

    west_panel = create_conference_panel(
        league.get_classement_west(), title="Conférence Ouest", color="blue"
    )
    east_panel = create_conference_panel(
        league.get_classement_east(), title="Conférence Est", color="red"
    )

    # Panel global avec 2 colonnes : Ouest à gauche, Est à droite
    main_table = Table.grid(expand=True)
    main_table.add_column()
    main_table.add_column()
    main_table.add_row(west_panel, east_panel)

    main_panel = Panel(
        main_table, title="Classement NBA", border_style="magenta", expand=True
    )
    console.print(main_panel)

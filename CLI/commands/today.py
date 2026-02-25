import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from core.schedule import Schedule  # adapte

console = Console()


def today():
    """
    Display today's NBA games in 2 columns.
    """

    schedule = Schedule()
    games = schedule.get_matchs_today()

    if not games:
        console.print(Panel("No games today 💤", border_style="yellow"))
        raise typer.Exit()

    table = Table.grid(expand=True)
    table.add_column()
    table.add_column()

    mds = []
    for game in games:
        md = Markdown(f"""
> **{game.awayTeam["teamName"]} @ {game.homeTeam["teamName"]}**
>
> 📅 {game.game_date}
>
> 📍 {game.arena}
""")
        mds.append(md)

    for i in range(0, len(mds), 2):
        left = mds[i]
        right = mds[i + 1] if i + 1 < len(mds) else ""
        table.add_row(left, right)

    main_panel = Panel(
        table, title="Matchs du jour", border_style="magenta", expand=True
    )

    console.print(main_panel)

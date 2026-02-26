import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()
app = typer.Typer(help="Afficher l'aide NBA CLI")

# Liste des commandes et descriptions
COMMANDS_INFO = [
    ("today", "Afficher les matchs d'aujourd'hui"),
    ("team info [TRICODE]", "Afficher les infos d'une équipe"),
    ("classement", "Afficher le classement NBA Est/Ouest"),
    ("help", "Afficher cette aide"),
]


@app.command()
def help_command():
    """
    Affiche toutes les commandes NBA disponibles avec un joli style.
    """
    table = Table.grid(expand=True)
    table.add_column(justify="left")
    table.add_column(justify="left")

    # Ajouter les commandes avec icône et description
    for cmd, desc in COMMANDS_INFO:
        md = Markdown(f"**nba {cmd}**")
        table.add_row(md, desc)

    # Encapsuler dans un panel principal
    main_panel = Panel(
        table,
        title="🏀 NBA CLI - Commandes disponibles",
        border_style="bright_blue",
        expand=True,
    )

    console.print(main_panel)

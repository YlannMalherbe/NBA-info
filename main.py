import typer

from CLI.commands import team
from CLI.commands.today import today  # today = fonction à l’intérieur du fichier

app = typer.Typer()
app.command()(today)

app.add_typer(team.app, name="team")

if __name__ == "__main__":
    app()

import typer

from CLI.commands import team
from CLI.commands.classement import classement
from CLI.commands.help import help_command
from CLI.commands.today import today
from core.schedule import ConnectionFailedError

app = typer.Typer()
app.command()(today)
app.command()(classement)
app.command(name="help")(help_command)

app.add_typer(team.app, name="team")

if __name__ == "__main__":
    try:
        app()
    except ConnectionFailedError as error:
        typer.secho(f"Erreur : {error}", fg=typer.colors.RED, err=True)
        raise SystemExit(1) from None

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from core.TeamData import TeamData

console = Console()


def display_info_team(team: TeamData):
    md = f"""
### 📊 Résultats

> **🏆 Wins**   : `{team.W}` W
>
> **❌ Losses** : `{team.L}` L
>
> **📈 Win %**  : `{team.get_winrate():.3f}` %

###  Prochain match

> **{team.get_next_match().awayTeam["teamName"]} @ {team.get_next_match().homeTeam["teamName"]}**
>
> 📅 {team.get_next_match().game_date.paris_date} à {team.get_next_match().game_date.paris_hour}
>
> 📍 {team.get_next_match().arena}


"""

    console.print(
        Panel(
            Markdown(md),
            title=f"[bold white]{team.team.full_name}",
            border_style="magenta",
        )
    )

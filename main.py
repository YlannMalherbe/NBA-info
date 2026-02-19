#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import requests

PARIS_TZ = ZoneInfo("Europe/Paris")
US_TZ = ZoneInfo("America/New_York")


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.nba.com/",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Affiche le(s) prochain(s) match(s) NBA"
    )

    parser.add_argument(
        "--team", default="SAS", help="Tricode de l'équipe NBA (ex: SAS, LAL, BOS)"
    )

    parser.add_argument(
        "--today", action="store_true", help="Affiche les matchs du jour"
    )

    return parser.parse_args()


def fetch_schedule() -> dict:
    """Renvoie le json contenant les informations et le planning des matches"""
    url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()


def parse_utc(dt_str: str) -> datetime:
    """Transforme une chaine de charactère en datetime"""
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))


def find_games(team: str, today: bool) -> list[dict]:
    now_utc = datetime.now(timezone.utc)
    now_us = now_utc.astimezone(US_TZ)

    schedule = fetch_schedule()
    candidates = []

    for day in schedule["leagueSchedule"]["gameDates"]:
        for game in day["games"]:
            teams = {
                game["homeTeam"]["teamTricode"],
                game["awayTeam"]["teamTricode"],
            }

            game_time_utc = parse_utc(game["gameDateTimeUTC"])
            game_time_us = game_time_utc.astimezone(US_TZ)

            if today:
                if game_time_us.date() == now_us.date():
                    candidates.append(game)
            else:
                if team in teams and game_time_utc > now_utc:
                    candidates.append((game_time_utc, game))

    if not candidates:
        raise RuntimeError("Aucun match trouvé.")

    if today:
        candidates.sort(key=lambda game: parse_utc(game["gameDateTimeUTC"]))
        return candidates

    candidates.sort(key=lambda x: x[0])
    return [candidates[0][1]]


def main():
    args = parse_args()
    team = args.team.upper()

    games = find_games(team, args.today)
    debut = True
    for game in games:
        game_time_utc = parse_utc(game["gameDateTimeUTC"])
        game_time_paris = game_time_utc.astimezone(PARIS_TZ)

        home = game["homeTeam"]["teamName"]
        away = game["awayTeam"]["teamName"]
        if debut:
            debut = False
            print("------------------------------------")
        print(f"Match : {away} @ {home}")
        print(
            game_time_paris.strftime(
                "Date : %A %d %B %Y\nHeure : %H:%M (heure française)"
            )
        )
        print("------------------------------------")


if __name__ == "__main__":
    main()

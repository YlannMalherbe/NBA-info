from dataclasses import dataclass
from enum import Enum


class Conference(Enum):
    EAST = "East"
    WEST = "West"


class Division(Enum):
    ATLANTIC = "Atlantic"
    CENTRAL = "Central"
    SOUTHEAST = "Southeast"
    NORTHWEST = "Northwest"
    PACIFIC = "Pacific"
    SOUTHWEST = "Southwest"


@dataclass(frozen=True, slots=True)
class Team:
    tricode: str
    city: str
    name: str
    conference: Conference
    division: Division

    def __post_init__(self):
        if len(self.tricode) != 3:
            raise ValueError("Le tricode doit contenir exactement 3 lettres.")
        object.__setattr__(self, "tricode", self.tricode.upper())

    @property
    def full_name(self) -> str:
        return f"{self.city} {self.name}"

    def is_east(self) -> bool:
        return self.conference is Conference.EAST

    def is_west(self) -> bool:
        return self.conference is Conference.WEST

    def __str__(self) -> str:
        return f"{self.full_name} ({self.tricode})"


NBA_TEAMS: dict[str, Team] = {

    # --- EASTERN CONFERENCE ---

    # Atlantic
    "BOS": Team("BOS", "Boston", "Celtics", Conference.EAST, Division.ATLANTIC),
    "BKN": Team("BKN", "Brooklyn", "Nets", Conference.EAST, Division.ATLANTIC),
    "NYK": Team("NYK", "New York", "Knicks", Conference.EAST, Division.ATLANTIC),
    "PHI": Team("PHI", "Philadelphia", "76ers", Conference.EAST, Division.ATLANTIC),
    "TOR": Team("TOR", "Toronto", "Raptors", Conference.EAST, Division.ATLANTIC),

    # Central
    "CHI": Team("CHI", "Chicago", "Bulls", Conference.EAST, Division.CENTRAL),
    "CLE": Team("CLE", "Cleveland", "Cavaliers", Conference.EAST, Division.CENTRAL),
    "DET": Team("DET", "Detroit", "Pistons", Conference.EAST, Division.CENTRAL),
    "IND": Team("IND", "Indiana", "Pacers", Conference.EAST, Division.CENTRAL),
    "MIL": Team("MIL", "Milwaukee", "Bucks", Conference.EAST, Division.CENTRAL),

    # Southeast
    "ATL": Team("ATL", "Atlanta", "Hawks", Conference.EAST, Division.SOUTHEAST),
    "CHA": Team("CHA", "Charlotte", "Hornets", Conference.EAST, Division.SOUTHEAST),
    "MIA": Team("MIA", "Miami", "Heat", Conference.EAST, Division.SOUTHEAST),
    "ORL": Team("ORL", "Orlando", "Magic", Conference.EAST, Division.SOUTHEAST),
    "WAS": Team("WAS", "Washington", "Wizards", Conference.EAST, Division.SOUTHEAST),

    # --- WESTERN CONFERENCE ---

    # Northwest
    "DEN": Team("DEN", "Denver", "Nuggets", Conference.WEST, Division.NORTHWEST),
    "MIN": Team("MIN", "Minnesota", "Timberwolves", Conference.WEST, Division.NORTHWEST),
    "OKC": Team("OKC", "Oklahoma City", "Thunder", Conference.WEST, Division.NORTHWEST),
    "POR": Team("POR", "Portland", "Trail Blazers", Conference.WEST, Division.NORTHWEST),
    "UTA": Team("UTA", "Utah", "Jazz", Conference.WEST, Division.NORTHWEST),

    # Pacific
    "GSW": Team("GSW", "Golden State", "Warriors", Conference.WEST, Division.PACIFIC),
    "LAC": Team("LAC", "Los Angeles", "Clippers", Conference.WEST, Division.PACIFIC),
    "LAL": Team("LAL", "Los Angeles", "Lakers", Conference.WEST, Division.PACIFIC),
    "PHX": Team("PHX", "Phoenix", "Suns", Conference.WEST, Division.PACIFIC),
    "SAC": Team("SAC", "Sacramento", "Kings", Conference.WEST, Division.PACIFIC),

    # Southwest
    "DAL": Team("DAL", "Dallas", "Mavericks", Conference.WEST, Division.SOUTHWEST),
    "HOU": Team("HOU", "Houston", "Rockets", Conference.WEST, Division.SOUTHWEST),
    "MEM": Team("MEM", "Memphis", "Grizzlies", Conference.WEST, Division.SOUTHWEST),
    "NOP": Team("NOP", "New Orleans", "Pelicans", Conference.WEST, Division.SOUTHWEST),
    "SAS": Team("SAS", "San Antonio", "Spurs", Conference.WEST, Division.SOUTHWEST),
}

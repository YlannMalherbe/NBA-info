from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo


US_TZ = ZoneInfo("America/New_York")
PARIS_TZ = ZoneInfo("Europe/Paris")


@dataclass(frozen=True, slots=True)
class GameDateTime:
    """
    Représente la date/heure officielle d’un match NBA.

    - Internement stockée en UTC (référence absolue).
    - Comparaison naturelle entre objets (chronologique).
    - Fournit des vues dans différents fuseaux (US / Paris).
    - Permet des tests d’inclusion (jour US, semaine, intervalle).

    Cette classe encapsule toute la logique temporelle afin
    d’éviter les erreurs liées aux fuseaux horaires.
    """

    _utc: datetime

    # -----------------------------
    # Construction
    # -----------------------------

    @classmethod
    def from_iso_utc(cls, iso_string: str) -> GameDateTime:
        """
        Construit un GameDateTime à partir d'une string ISO en UTC
        (ex: '2026-01-15T00:30:00Z').
        """
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            raise ValueError("La date ISO doit être timezone-aware.")
        return cls(dt.astimezone(timezone.utc))

    @classmethod
    def now(cls) -> GameDateTime:
        """Retourne l’instant présent en UTC."""
        return cls(datetime.now(timezone.utc))

    # -----------------------------
    # Propriétés principales
    # -----------------------------

    @property
    def utc(self) -> datetime:
        """Date/heure UTC (référence absolue)."""
        return self._utc

    @property
    def us(self) -> datetime:
        """Date/heure convertie en Eastern Time (NBA reference)."""
        return self._utc.astimezone(US_TZ)

    @property
    def paris(self) -> datetime:
        """Date/heure convertie en heure française."""
        return self._utc.astimezone(PARIS_TZ)

    @property
    def us_date(self):
        """Date (année/mois/jour) en heure US."""
        return self.us.date()

    @property
    def paris_date(self):
        """Date en heure française."""
        return self.paris.date()

    @property
    def us_time(self):
        """Heure (HH:MM:SS) en Eastern Time."""
        return self.us.time()

    @property
    def paris_time(self):
        """Heure (HH:MM:SS) en heure française."""
        return self.paris.time()

    @property
    def us_hour(self) -> str:
        """Heure formatée HH:MM en Eastern Time."""
        return self.us.strftime("%H:%M")

    @property
    def paris_hour(self) -> str:
        """Heure formatée HH:MM en heure de Paris."""
        return self.paris.strftime("%H:%M")

    def get_hours(self) -> dict[str, str]:
        """
        Retourne les heures formatées US et Paris.
        """
        return {
            "us": self.us_hour,
            "paris": self.paris_hour,
        }

    # -----------------------------
    # Comparaisons naturelles
    # -----------------------------

    def __lt__(self, other: GameDateTime) -> bool:
        return self._utc < other._utc

    def __le__(self, other: GameDateTime) -> bool:
        return self._utc <= other._utc

    def __gt__(self, other: GameDateTime) -> bool:
        return self._utc > other._utc

    def __ge__(self, other: GameDateTime) -> bool:
        return self._utc >= other._utc

    def __eq__(self, other: object) -> bool:
        return self._utc == other._utc

    # -----------------------------
    # Méthodes métier utiles
    # -----------------------------

    def is_same_us_day(self, other: GameDateTime) -> bool:
        """Retourne True si les deux instants sont le même jour US."""
        return self.us_date == other.us_date

    def is_today_us(self) -> bool:
        """True si le match est aujourd'hui (jour NBA US)."""
        return self.us_date == GameDateTime.now().us_date

    def is_in_week_us(self, reference: GameDateTime | None = None) -> bool:
        """
        Vérifie si le match est dans la même semaine US
        que la date de référence (par défaut aujourd'hui).
        """
        if reference is None:
            reference = GameDateTime.now()

        start_of_week = reference.us - timedelta(days=reference.us.weekday())
        end_of_week = start_of_week + timedelta(days=7)

        return start_of_week.date() <= self.us_date < end_of_week.date()

    def is_between(self, start: GameDateTime, end: GameDateTime) -> bool:
        """
        Vérifie si l’instant est compris dans [start, end].
        """
        return start <= self <= end

    # -----------------------------
    # Représentation
    # -----------------------------

    def __str__(self) -> str:
        return f'{self.paris_date} {self.paris_time} (Paris)'

    def __repr__(self) -> str:
        return f"GameDateTime(utc={self._utc.isoformat()})"

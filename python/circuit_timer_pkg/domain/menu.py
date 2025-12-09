"""Domain objects for training menus and duration parsing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class TrainingMenu:
    name: str
    set_seconds: int
    rest_seconds: int
    sets: int

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "TrainingMenu":
        return cls(
            name=str(data["name"]),
            set_seconds=int(data["set_seconds"]),
            rest_seconds=int(data["rest_seconds"]),
            sets=int(data["sets"]),
        )

    def to_dict(self) -> Dict[str, int | str]:
        return {
            "name": self.name,
            "set_seconds": self.set_seconds,
            "rest_seconds": self.rest_seconds,
            "sets": self.sets,
        }


def format_time(seconds: int) -> str:
    minutes, secs = divmod(max(0, int(seconds)), 60)
    return f"{minutes:02d}:{secs:02d}"


def parse_duration(value: str) -> int:
    raw = value.strip().lower()
    if not raw:
        raise ValueError("値を入力してください。")

    def _to_seconds(number: float) -> int:
        seconds = int(number)
        if seconds <= 0:
            raise ValueError
        return seconds

    try:
        if raw.endswith("m"):
            minutes = float(raw[:-1])
            return _to_seconds(minutes * 60)
        if raw.endswith("s"):
            return _to_seconds(float(raw[:-1]))
        return _to_seconds(float(raw))
    except ValueError as exc:
        raise ValueError("数値または 30s / 0.5m 形式で入力してください。") from exc

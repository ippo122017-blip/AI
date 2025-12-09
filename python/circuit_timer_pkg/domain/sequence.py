"""Timer phase utilities."""

from __future__ import annotations

from typing import Iterable, List, NamedTuple

from .menu import TrainingMenu


class Phase(NamedTuple):
    label: str
    duration: int
    set_index: int
    total_sets: int


def build_sequence(menu: TrainingMenu) -> List[Phase]:
    phases: List[Phase] = []
    for idx in range(1, menu.sets + 1):
        phases.append(Phase("作業", menu.set_seconds, idx, menu.sets))
        if idx < menu.sets and menu.rest_seconds > 0:
            phases.append(Phase("休憩", menu.rest_seconds, idx, menu.sets))
    return phases


def total_duration(phases: Iterable[Phase]) -> int:
    return sum(phase.duration for phase in phases)

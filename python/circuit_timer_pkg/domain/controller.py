"""Simple timer controller independent from UI frameworks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional

from .menu import TrainingMenu
from .sequence import Phase, build_sequence, total_duration

TickCallback = Callable[[Phase, int, int], None]
EventCallback = Callable[[Phase], None]


@dataclass
class TimerController:
    on_phase_start: Optional[EventCallback] = None
    on_tick: Optional[TickCallback] = None
    on_complete: Optional[Callable[[], None]] = None

    sequence: List[Phase] = field(default_factory=list)
    total_seconds: int = 0
    elapsed_seconds: int = 0
    current_index: int = 0
    remaining: int = 0
    running: bool = False

    def load_menu(self, menu: TrainingMenu) -> None:
        self.sequence = build_sequence(menu)
        self.total_seconds = total_duration(self.sequence)
        self.elapsed_seconds = 0
        self.current_index = 0
        self.remaining = self.sequence[0].duration if self.sequence else 0
        self.running = False

    def start(self) -> None:
        if not self.sequence:
            raise ValueError("シーケンスが設定されていません。")
        self.elapsed_seconds = 0
        self.current_index = 0
        self.remaining = self.sequence[0].duration
        self.running = True
        self._emit_phase_start()

    def stop(self) -> None:
        self.running = False
        self.elapsed_seconds = 0
        self.remaining = 0
        self.current_index = 0

    def tick(self, seconds: int = 1) -> None:
        if not self.running:
            return
        self.remaining -= seconds
        self.elapsed_seconds += seconds
        if self.remaining <= 0:
            self.current_index += 1
            if self.current_index >= len(self.sequence):
                self.running = False
                if self.on_complete:
                    self.on_complete()
                return
            self.remaining = self.sequence[self.current_index].duration
            self._emit_phase_start()
        if self.on_tick:
            self.on_tick(self.sequence[self.current_index], self.remaining, self.elapsed_seconds)

    def current_phase(self) -> Optional[Phase]:
        if not self.sequence or self.current_index >= len(self.sequence):
            return None
        return self.sequence[self.current_index]

    def _emit_phase_start(self) -> None:
        if self.on_phase_start and self.sequence:
            self.on_phase_start(self.sequence[self.current_index])
        if self.on_tick:
            self.on_tick(self.sequence[self.current_index], self.remaining, self.elapsed_seconds)

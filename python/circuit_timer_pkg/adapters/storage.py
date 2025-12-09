"""Persistence helpers for training menus."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from ..circuit_paths import MENU_FILE
from ..domain.menu import TrainingMenu


def load_menus(file_path: Path | None = None) -> Dict[str, TrainingMenu]:
    path = file_path or MENU_FILE
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    menus: Dict[str, TrainingMenu] = {}
    for item in data:
        menu = TrainingMenu.from_dict(item)
        menus[menu.name] = menu
    return menus


def save_menus(menus: Dict[str, TrainingMenu], file_path: Path | None = None) -> None:
    path = file_path or MENU_FILE
    payload = [menu.to_dict() for menu in menus.values()]
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

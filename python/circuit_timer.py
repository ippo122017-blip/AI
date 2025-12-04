"""Circuit training timer CLI application."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional

MENU_FILE = Path(__file__).with_name("menus.json")


@dataclass
class TrainingMenu:
    """シンプルなメニュー構造"""

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


def load_menus() -> Dict[str, TrainingMenu]:
    """JSON からメニュー一覧を読み込む"""

    if not MENU_FILE.exists():
        return {}
    data = json.loads(MENU_FILE.read_text(encoding="utf-8"))
    menus = {}
    for item in data:
        menu = TrainingMenu.from_dict(item)
        menus[menu.name] = menu
    return menus


def save_menus(menus: Dict[str, TrainingMenu]) -> None:
    """メニュー一覧を JSON に保存"""

    payload = [asdict(menu) for menu in menus.values()]
    MENU_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def prompt_seconds(prompt: str) -> int:
    """s/m の単位付き入力を秒に変換"""

    while True:
        raw = input(prompt).strip().lower()
        if not raw:
            print("値を入力してください。")
            continue
        try:
            if raw.endswith("m"):
                minutes = float(raw[:-1])
                return int(minutes * 60)
            if raw.endswith("s"):
                return int(float(raw[:-1]))
            return int(float(raw))
        except ValueError:
            print("数値または 30s / 0.5m 形式で入力してください。")


def prompt_int(prompt: str, min_value: int = 1) -> int:
    """整数入力をバリデーション"""

    while True:
        raw = input(prompt).strip()
        if not raw:
            print("値を入力してください。")
            continue
        try:
            value = int(raw)
            if value < min_value:
                raise ValueError
            return value
        except ValueError:
            print(f"{min_value} 以上の整数で入力してください。")


def create_menu(existing: Dict[str, TrainingMenu]) -> TrainingMenu:
    """ユーザーと対話してメニューを作成"""

    print("\n--- 新しいメニューの作成 ---")
    while True:
        name = input("メニュー名: ").strip()
        if not name:
            print("メニュー名を入力してください。")
            continue
        if name in existing:
            overwrite = input("同名のメニューがあります。上書きしますか? (y/n): ").lower()
            if overwrite != "y":
                continue
        break

    set_seconds = prompt_seconds("1セットの時間 (例: 45s, 1.5m): ")
    rest_seconds = prompt_seconds("休憩時間 (例: 15s, 1m): ")
    sets = prompt_int("セット数: ", min_value=1)

    return TrainingMenu(name=name, set_seconds=set_seconds, rest_seconds=rest_seconds, sets=sets)


def choose_menu(menus: Dict[str, TrainingMenu]) -> Optional[TrainingMenu]:
    """保存済みメニューから選択"""

    if not menus:
        print("保存済みメニューがありません。")
        return None

    print("\n--- メニュー一覧 ---")
    names = list(menus.keys())
    for idx, name in enumerate(names, start=1):
        menu = menus[name]
        print(f"{idx}. {menu.name} | セット: {menu.sets}, 作業: {menu.set_seconds}s, 休憩: {menu.rest_seconds}s")

    while True:
        choice = input("番号を入力してください (キャンセルは Enter): ").strip()
        if not choice:
            return None
        if not choice.isdigit():
            print("数字で入力してください。")
            continue
        index = int(choice)
        if 1 <= index <= len(names):
            return menus[names[index - 1]]
        print("範囲内の番号を選んでください。")


def countdown(label: str, seconds: int) -> None:
    """ラベル付きカウントダウン表示"""

    for remaining in range(seconds, 0, -1):
        print(f"{label}: 残り {remaining:02d} 秒", end="\r", flush=True)
        time.sleep(1)
    print(f"{label}: 完了{' ' * 10}")


def run_timer(menu: TrainingMenu) -> None:
    """メニューに従ってタイマーを進行"""

    print(f"\n=== {menu.name} を開始 ===")
    for current_set in range(1, menu.sets + 1):
        print(f"\nセット {current_set}/{menu.sets} - 作業開始")
        countdown("作業", menu.set_seconds)
        if current_set < menu.sets:
            print("休憩に入ります")
            countdown("休憩", menu.rest_seconds)
    print("\nおつかれさまでした！")


def main() -> None:
    """アプリのメインループ"""

    menus = load_menus()

    while True:
        print("\n=== サーキットタイマー ===")
        print("1. メニュー作成/上書き")
        print("2. メニュー一覧")
        print("3. メニューを選んでタイマー開始")
        print("4. 終了")
        choice = input("選択肢: ").strip()

        if choice == "1":
            menu = create_menu(menus)
            menus[menu.name] = menu
            save_menus(menus)
            print(f"'{menu.name}' を保存しました。")
        elif choice == "2":
            if menus:
                choose_menu(menus)
            else:
                print("保存済みメニューがありません。")
        elif choice == "3":
            menu = choose_menu(menus)
            if menu:
                run_timer(menu)
        elif choice == "4":
            print("終了します。")
            break
        else:
            print("1-4の数字を入力してください。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n中断しました。")

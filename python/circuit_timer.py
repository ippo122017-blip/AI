"""Circuit training timer application with CLI and Tkinter UI."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

try:  # Tkinter is optional so the CLI can still run.
    import tkinter as tk
    from tkinter import messagebox, ttk
except Exception:  # pragma: no cover - helps when Tk is missing.
    tk = None
    messagebox = None
    ttk = None

MENU_FILE = Path(__file__).with_name("menus.json")


def format_time(seconds: int) -> str:
    """Return an mm:ss string for the given seconds."""

    minutes, secs = divmod(max(0, int(seconds)), 60)
    return f"{minutes:02d}:{secs:02d}"


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


def parse_duration(value: str) -> int:
    """Parse values like '45', '45s', '1.5m' into seconds."""

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
        raw = input(prompt).strip()
        try:
            return parse_duration(raw)
        except ValueError as exc:
            print(exc)


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


def run_cli() -> None:
    """アプリのメインループ (CLI)"""

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


Phase = Tuple[str, int, int, int]


class CircuitTimerApp:
    """Tkinter UI to manage menus and run the timer."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("サーキットタイマー")
        self.root.geometry("760x450")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.colors = {
            "bg": "#0f172a",
            "card": "#1e293b",
            "accent": "#2563eb",
            "accent_hover": "#1d4ed8",
            "text": "#f8fafc",
            "muted": "#94a3b8",
        }
        self.root.configure(background=self.colors["bg"])
        self._configure_styles()

        self.menus: Dict[str, TrainingMenu] = load_menus()
        self.current_names: List[str] = []

        self.name_var = tk.StringVar()
        self.set_var = tk.StringVar(value="45")
        self.rest_var = tk.StringVar(value="15")
        self.sets_var = tk.StringVar(value="3")

        self.status_var = tk.StringVar(value="メニューを選択してください。")
        self.timer_var = tk.StringVar(value="タイマー停止中")

        self.timer_running = False
        self.sequence: List[Phase] = []
        self.current_phase_index = 0
        self.remaining = 0
        self.total_duration = 0
        self.elapsed_total = 0
        self.active_menu_name: Optional[str] = None
        self.after_id: Optional[str] = None

        self._build_layout()
        self.refresh_menu_list()

    def _configure_styles(self) -> None:
        bg = self.colors["bg"]
        card = self.colors["card"]
        accent = self.colors["accent"]
        accent_hover = self.colors["accent_hover"]
        text = self.colors["text"]
        muted = self.colors["muted"]

        self.style.configure("Main.TFrame", background=bg)
        self.style.configure(
            "Card.TLabelframe",
            background=card,
            foreground=text,
            borderwidth=0,
            padding=12,
        )
        self.style.configure("Card.TLabelframe.Label", background=card, foreground=muted)
        self.style.configure("Side.TFrame", background=card)
        self.style.configure("Heading.TLabel", background=card, foreground=text, font=("Segoe UI", 14, "bold"))
        self.style.configure("Body.TLabel", background=card, foreground=text, font=("Segoe UI", 11))
        self.style.configure("Status.TLabel", background=card, foreground=muted, font=("Segoe UI", 11))
        self.style.configure(
            "Accent.TButton",
            background=accent,
            foreground=text,
            padding=8,
            font=("Segoe UI", 10, "bold"),
        )
        self.style.map(
            "Accent.TButton",
            background=[("active", accent_hover), ("pressed", accent_hover)],
            foreground=[("disabled", muted)],
        )
        self.style.configure(
            "Modern.TButton",
            background=card,
            foreground=text,
            padding=6,
            font=("Segoe UI", 10),
        )
        self.style.map(
            "Modern.TButton",
            background=[("active", "#334155"), ("pressed", "#1e293b")],
            foreground=[("disabled", muted)],
        )
        self.style.configure(
            "Timer.TLabel",
            background=card,
            foreground=text,
            font=("Segoe UI", 32, "bold"),
        )
        self.style.configure(
            "Accent.Horizontal.TProgressbar",
            troughcolor="#0b1220",
            background=accent,
            bordercolor=card,
            lightcolor=accent,
            darkcolor=accent,
        )

    def _build_layout(self) -> None:
        main = ttk.Frame(self.root, padding=16, style="Main.TFrame")
        main.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        list_frame = ttk.Frame(main, padding=12, style="Side.TFrame")
        list_frame.grid(row=0, column=0, sticky="ns")

        ttk.Label(list_frame, text="メニュー一覧", style="Heading.TLabel").pack(anchor="w")
        self.menu_list = tk.Listbox(
            list_frame,
            height=14,
            width=32,
            exportselection=False,
            bg=self.colors["card"],
            fg=self.colors["text"],
            highlightthickness=0,
            bd=0,
            selectbackground=self.colors["accent"],
            selectforeground=self.colors["text"],
            font=("Segoe UI", 11),
        )
        self.menu_list.pack(fill="both", expand=True, pady=(4, 6))
        self.menu_list.bind("<<ListboxSelect>>", lambda _event: self.on_select_menu())

        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="タイマー開始", style="Accent.TButton", command=self.start_timer).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="タイマー停止", style="Modern.TButton", command=self.stop_timer).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="選択メニュー削除", style="Modern.TButton", command=self.delete_menu).pack(fill="x", pady=2)

        form = ttk.LabelFrame(main, text="メニューの編集", style="Card.TLabelframe")
        form.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="名前", style="Body.TLabel").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Entry(form, textvariable=self.name_var, font=("Segoe UI", 11)).grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(form, text="セットの時間 (秒 / 45s / 1.5m)", style="Body.TLabel").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(form, textvariable=self.set_var, font=("Segoe UI", 11)).grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(form, text="休憩の時間 (秒 / 30s / 1m)", style="Body.TLabel").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(form, textvariable=self.rest_var, font=("Segoe UI", 11)).grid(row=2, column=1, sticky="ew", pady=2)

        ttk.Label(form, text="セット数", style="Body.TLabel").grid(row=3, column=0, sticky="w", pady=2)
        ttk.Entry(form, textvariable=self.sets_var, font=("Segoe UI", 11)).grid(row=3, column=1, sticky="ew", pady=2)

        ttk.Button(form, text="保存 / 上書き", style="Accent.TButton", command=self.save_menu).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        timer_frame = ttk.LabelFrame(main, text="タイマー", style="Card.TLabelframe")
        timer_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(16, 0))

        ttk.Label(timer_frame, textvariable=self.status_var, style="Heading.TLabel").pack(anchor="w")
        ttk.Label(timer_frame, textvariable=self.timer_var, style="Status.TLabel").pack(anchor="w", pady=(2, 8))
        self.timer_display = ttk.Label(timer_frame, text="00:00", style="Timer.TLabel")
        self.timer_display.pack(anchor="center", pady=(4, 8))
        self.progress = ttk.Progressbar(timer_frame, style="Accent.Horizontal.TProgressbar", mode="determinate", maximum=1, value=0)
        self.progress.pack(fill="x")

    def refresh_menu_list(self, select_name: Optional[str] = None) -> None:
        self.menu_list.delete(0, tk.END)
        self.current_names = sorted(self.menus.keys())
        for name in self.current_names:
            menu = self.menus[name]
            summary = f"{name} | {menu.sets}セット ({menu.set_seconds}s / {menu.rest_seconds}s)"
            self.menu_list.insert(tk.END, summary)
        if select_name and select_name in self.menus:
            idx = self.current_names.index(select_name)
            self.menu_list.selection_clear(0, tk.END)
            self.menu_list.selection_set(idx)
            self.menu_list.see(idx)
            self.on_select_menu()
        elif not self.current_names:
            self.clear_form()

    def on_select_menu(self) -> None:
        index = self._selected_index()
        if index is None:
            return
        name = self.current_names[index]
        menu = self.menus[name]
        self.name_var.set(menu.name)
        self.set_var.set(str(menu.set_seconds))
        self.rest_var.set(str(menu.rest_seconds))
        self.sets_var.set(str(menu.sets))
        self.status_var.set(f"選択中: {menu.name}")

    def save_menu(self) -> None:
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("エラー", "メニュー名を入力してください。")
            return
        try:
            set_seconds = parse_duration(self.set_var.get())
            rest_seconds = parse_duration(self.rest_var.get())
            sets = int(self.sets_var.get())
            if sets < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("エラー", "時間は数値 (例: 45 / 45s / 1.5m)、セット数は1以上の整数で入力してください。")
            return

        menu = TrainingMenu(name=name, set_seconds=set_seconds, rest_seconds=rest_seconds, sets=sets)
        self.menus[name] = menu
        save_menus(self.menus)
        self.refresh_menu_list(select_name=name)
        messagebox.showinfo("保存", f"'{name}' を保存しました。")

    def delete_menu(self) -> None:
        index = self._selected_index()
        if index is None:
            messagebox.showwarning("削除", "メニューを選択してください。")
            return
        name = self.current_names[index]
        if not messagebox.askyesno("確認", f"'{name}' を削除しますか？"):
            return
        self.menus.pop(name, None)
        save_menus(self.menus)
        self.refresh_menu_list()
        messagebox.showinfo("削除", f"'{name}' を削除しました。")

    def start_timer(self) -> None:
        if self.timer_running:
            messagebox.showinfo("タイマー", "すでにタイマーが動作しています。")
            return
        index = self._selected_index()
        if index is None:
            messagebox.showwarning("タイマー", "メニューを選択してください。")
            return
        name = self.current_names[index]
        menu = self.menus[name]
        self.sequence = list(self._build_sequence(menu))
        if not self.sequence:
            messagebox.showwarning("タイマー", "有効なシーケンスがありません。")
            return
        self.active_menu_name = menu.name
        self.current_phase_index = 0
        self.remaining = self.sequence[0][1]
        self.total_duration = sum(phase[1] for phase in self.sequence)
        self.progress.configure(maximum=max(1, self.total_duration))
        self.elapsed_total = 0
        self.progress.configure(value=0)
        self.timer_running = True
        self.status_var.set(f"{menu.name} を開始")
        self._update_timer_label()
        self._update_progress()
        self._schedule_tick()

    def _build_sequence(self, menu: TrainingMenu) -> Sequence[Phase]:
        phases: List[Phase] = []
        for idx in range(1, menu.sets + 1):
            phases.append(("作業", menu.set_seconds, idx, menu.sets))
            if idx < menu.sets and menu.rest_seconds > 0:
                phases.append(("休憩", menu.rest_seconds, idx, menu.sets))
        return phases

    def _schedule_tick(self) -> None:
        self.after_id = self.root.after(1000, self._tick)

    def _tick(self) -> None:
        if not self.timer_running:
            return
        self.remaining -= 1
        self.elapsed_total += 1
        if self.remaining <= 0:
            self.current_phase_index += 1
            if self.current_phase_index >= len(self.sequence):
                self._finish_timer()
                return
            self.remaining = self.sequence[self.current_phase_index][1]
        self._update_timer_label()
        self._update_progress()
        self._schedule_tick()

    def _update_timer_label(self) -> None:
        if not self.timer_running or not self.sequence:
            self.timer_var.set("タイマー停止中")
            self.timer_display.configure(text="00:00")
            return
        label, _seconds, set_number, total_sets = self.sequence[self.current_phase_index]
        self.timer_var.set(f"{label} - セット {set_number}/{total_sets}: 残り {self.remaining:02d} 秒")
        self.timer_display.configure(text=format_time(self.remaining))

    def _finish_timer(self) -> None:
        self.timer_running = False
        self.sequence = []
        self.current_phase_index = 0
        self.remaining = 0
        self.elapsed_total = 0
        self.timer_var.set("完了！")
        if self.active_menu_name:
            self.status_var.set(f"{self.active_menu_name} 完了！")
        if messagebox:
            messagebox.showinfo("タイマー", "おつかれさまでした！")
        self.active_menu_name = None
        self.timer_display.configure(text="00:00")
        self.progress.configure(value=0)

    def stop_timer(self) -> None:
        if not self.timer_running:
            self.timer_var.set("タイマー停止中")
            return
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.timer_running = False
        self.sequence = []
        self.timer_var.set("停止しました")
        self.status_var.set("タイマーを停止しました。")
        self.elapsed_total = 0
        self.timer_display.configure(text="00:00")
        self.progress.configure(value=0)

    def _update_progress(self) -> None:
        if self.total_duration <= 0:
            self.progress.configure(value=0)
            return
        value = min(self.elapsed_total, self.total_duration)
        self.progress.configure(value=value)

    def clear_form(self) -> None:
        self.name_var.set("")
        self.set_var.set("45")
        self.rest_var.set("15")
        self.sets_var.set("3")
        self.status_var.set("メニューを選択してください。")

    def _selected_index(self) -> Optional[int]:
        if not self.current_names:
            return None
        selection = self.menu_list.curselection()
        if not selection:
            return None
        index = selection[0]
        if index >= len(self.current_names):
            return None
        return index


def run_ui() -> None:
    if tk is None or messagebox is None or ttk is None:
        raise RuntimeError("Tkinter が利用できないため、UI モードを開始できません。Python を 'tk' サポート付きでインストールしてください。")
    root = tk.Tk()
    CircuitTimerApp(root)
    root.mainloop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Circuit training timer")
    parser.add_argument("--cli", action="store_true", help="CLI モードで起動")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.cli:
        try:
            run_cli()
        except KeyboardInterrupt:
            print("\n中断しました。")
    else:
        run_ui()


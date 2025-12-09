# circuit_timer.py リファクタリング計画

最終更新: 2025-12-09

## 1. 目的
- CLI/Tkinter実装に埋め込まれているビジネスロジック（メニュー管理、タイマーシーケンス、時間計算）を分離し、将来のモバイル実装で再利用可能な形にする。
- テスト容易性とコードの見通し改善。

## 2. 現状課題
- メニュー読み書き、CLI入出力、Tkinter UIが単一ファイルに集中し200+行超。
- ロジックとUI（print/tkinter）が強く結合し、単体テスト困難。
- タイマーは`run_timer`や`CircuitTimerApp._tick`内で直接`time.sleep`や`after`を呼んでいる。

## 3. ターゲット構成
```
python/
  circuit_timer/
    __init__.py
    domain/
      menu.py        # TrainingMenu, validation
      sequence.py    # Phase生成, TimerSequence
      controller.py  # TimerController, start/pause/stop
    adapters/
      storage.py     # JSON <-> domain
      cli.py         # 既存CLIのUI層
      tk_ui.py       # Tkinter UI (現行移植)
```

## 4. ステップ
| No | 内容 | 詳細 | 成果物 |
|----|------|------|--------|
| R-01 | プロジェクト構造をディレクトリ化 | `python/circuit_timer/`パッケージを作り、既存ファイルを分割する準備。 | 新ディレクトリ/`__init__.py` |
| R-02 | ドメインオブジェクト移行 | `TrainingMenu`, `parse_duration`, `Phase`生成を`domain`に移し、UI依存を排除。 | `domain/menu.py`, `domain/sequence.py` |
| R-03 | タイマーコントローラ作成 | 現行CLI/Tkの進行ロジックを抽象クラスにまとめ、依存注入（tickコールバック）でUIと分離。 | `domain/controller.py` |
| R-04 | ストレージ層実装 | JSONファイルアクセスを`adapters/storage.py`に切り出し、今後のDB/API置換に備える。 | `adapters/storage.py` |
| R-05 | CLIの再配線 | `cli.py`でドメイン層を利用するよう書き換え、入出力のみ担う。 | `cli.py` |
| R-06 | Tk UIの再配線 | `tk_ui.py`でドメイン層を利用し、UIイベント→コントローラ呼び出しに変更。 | `tk_ui.py` |
| R-07 | 旧`circuit_timer.py`整理 | 入口スクリプトとしてCLI/GUI切り替えのみ保持。 | 200行未満に縮小 |
| R-08 | テスト追加 | `tests/test_domain.py`で`parse_duration`, `TimerController`などを検証。 | pytestテスト |

## 5. 段階的進め方
1. R-01〜R-03でドメイン完成 → 単体テスト。
2. R-04でストレージ抽象化。
3. CLI (R-05) → Tk UI (R-06) の順に置き換え。
4. 最後に旧ファイル整理とエントリーポイント更新 (R-07)。
5. pytest導入し、CIで回す (R-08)。

## 6. 注意点
- 既存`menus.json`互換を維持。ファイルパスは従来通り。
- CLIとTk UIの挙動を保つため、既存関数のユーザーI/Oメッセージは維持。
- タイマーのsleep/afterを抽象化し、将来asyncや別UIにも流用できるインターフェースを検討。

## 7. 次アクション
- `python/circuit_timer/`ディレクトリ作成 (R-01)。
- `TrainingMenu`と関連関数を`domain/menu.py`にコピーし、既存コードから参照させる。

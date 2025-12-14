# Flutter セットアップ手順 (ローカル環境)
最終更新: 2025-12-09

1. **SDK取得**
   - https://docs.flutter.dev/get-started/install/windows から Flutter SDK (3.24+ stable) をダウンロード。
   - 例: `C:\dev\flutter` に展開し、`flutter\bin` をPATHへ追加。
2. **依存インストール**
   - Android Studio + Android SDK、必要なplatform-toolsをセットアップ。
   - `flutter doctor --android-licenses` を実行しライセンス同意。
   - VS Code か Android Studio に Flutter/Dart プラグインをインストール。
3. **確認**
   - PowerShellで `flutter doctor` がエラーなく完了することを確認。
4. **プロジェクト作成**
   - このリポジトリ内 `python/flutter_timer_poc` を作業ディレクトリにし、`flutter create circuit_timer_mvp` を実行。
   - 以降のコードは `python/flutter_timer_poc/circuit_timer_mvp` 配下で管理。
5. **端末接続**
   - Android実機をUSB接続し、USBデバッグON。`flutter devices` で認識を確認。
6. **PoC実行**
   - `flutter run` で雛形を起動→`docs/flutter_timer_poc_plan.md` P-01〜P-03 を順に着手。

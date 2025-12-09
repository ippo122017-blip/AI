# サーキットタイマー モバイル技術選定メモ

最終更新: 2025-12-06

## 1. ゴール
- iOS/Android両対応でMVPを短期間に実装し、精度±0.1秒のタイマー、通知・振動・バックグラウンド実行、ローカルDB、将来的なクラウド同期を実現できる技術スタックを選定する。
- 個人開発（単独）で学習コストを抑えつつ保守運用しやすいこと。

## 2. 評価軸
| 軸 | 内容 |
|----|------|
| 開発速度 | UI/状態管理/通知を短期間で形にできるか。
| パフォーマンス | タイマー精度、アニメーション、低レイテンシ通知。
| ネイティブ連携 | 通知/振動/バックグラウンド/センサーAPIへのアクセス容易性。
| エコシステム | ライブラリ、ドキュメント、学習リソース。
| 再利用性 | 将来のWeb/デスクトップ展開や既存Pythonロジックとの親和性。
| メンテ性 | コード量、ホットリロード、テスト支援。

## 3. 候補比較
| 項目 | Flutter | React Native | ネイティブ(Swift+Kotlin) | Kotlin Multiplatform + SwiftUI |
|------|---------|--------------|----------------------------|------------------------------|
| 開発速度 | ◎ Hot Reload、豊富なUI部品 | ○ JS/TSで迅速、要Bridge管理 | △ 両OS別実装で時間倍増 | △ 共通ロジックは共有可だがUI2回実装 |
| パフォーマンス/描画 | ◎ Skia描画で一貫、高FPS | ○ Fabric導入済でもJS Bridge負荷 | ◎ 完全ネイティブ | ○ ただしUIは個別 |
| ネイティブAPI | ○ Platform Channelでラップ必要 | ○ Native Module実装 | ◎ 直接利用 | ○ 共有ロジック+Platform依存コードで実装 |
| 学習コスト(個人) | ○ Dart+Flutter学習 | ○ React/JS経験あれば低 | △ Swift/Kotlin両方必要 | △ Kotlin/Swift双方の知識とKMP知見 |
| コードシェア/保守 | ◎ 単一コードベース | ○ JS/TS+Native Module | △ 共通化ほぼ無し | ○ ドメイン共有可だがUI重複 |
| タイマー精度/背後実行 | ◎ `flutter_local_notifications`/`android_alarm_manager_plus`等で実績 | ○ 可能だがModule整備必要 | ◎ OS機能を直接利用 | ○ 設計次第 |
| 今後の拡張（Web/デスクトップ） | ○ FlutterはWeb/Windows/macOSにも展開可 | △ React Native for Webは別対応 | △ 各OS別 | △ 複雑 |

## 4. 推奨案
- **Flutter**を第一候補とする。
  - 単一コードベースでUI・状態管理・ロジックをまとめられ、個人開発での速度が出しやすい。
  - 通知/振動/バックグラウンドタスク向けの成熟したプラグインが揃い、Skia描画でタイマーUIを滑らかに実装可能。
  - 将来のWeb/デスクトップ対応余地も確保できる。
- React Nativeは既存JS資産がある場合の代替案。ネイティブ(Swift/Kotlin)は最高制御だが工数が倍になるため、将来の最適化フェーズまで保留。KMPはチーム拡大後に検討。

## 5. Flutter採用時の補足
- 状態管理: RiverpodまたはBloc。テスト容易性と可読性を優先。
- ローカルDB: `isar` or `floor` + `sqlite`. JSONインポート/エクスポート用に`freezed`でモデル生成。
- 通知: `flutter_local_notifications`で前景/背景の通知、`awesome_notifications`でカスタム振動。
- バックグラウンド: Androidは`android_alarm_manager_plus`+ForegroundService、iOSは`Workmanager`と通知スケジュールで対応。
- CI/CD: `codemagic`や`GitHub Actions`でビルド自動化を検討。

## 6. React Nativeを選ぶ場合の留意点
- 新Architecture(Fabric+TurboModules)を前提にし、`react-native-push-notification`などネイティブモジュールを検証。
- TypeScript + Zustand/Recoilで状態を管理し、JS Bridge越しのタイマー精度に注意。重大処理はNative Module化が必要。

## 7. ネイティブ(Swift/Kotlin)案を採らない理由
- 個人開発で2コードベースは工数・保守コストが高い。
- ただしOS固有の高度なヘルス連携やWear対応が最優先になった場合は再検討。

## 8. 次のアクション
1. Flutterでタイマー/通知PoCを実装（1〜2日想定）し、±0.1秒精度とバックグラウンド挙動を検証。
2. プロトタイピングで得た知見を本メモと要件ドキュメントにフィードバック。
3. 問題があればReact Native/ネイティブ案を再評価し、リスク/工数を比較。

---
このメモは技術選定の意思決定ログとして利用し、主要な設計変更時に更新してください。

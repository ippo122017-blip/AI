# Flutter Timer/Notification PoC Plan

Last Updated: 2025-12-09

## 1. Objective
- Verify that Flutter can deliver a circuit timer with ±0.1s accuracy, notifications, vibration, and background continuity.
- Surface plugin/architecture risks before committing to the stack.

## 2. Scope
- Platforms: Android 14 (device/emulator), iOS 17 (simulator, later device).
- Features: fixed menu definition, start/pause/stop, local notifications, vibration, resume after background.
- Out of scope: persistence, sync, history UI, polished visuals.

## 3. Setup
1. Install Flutter SDK 3.24+.
2. Plugins: flutter_local_notifications, awesome_notifications, android_alarm_manager_plus, workmanager, vibration, riverpod.
3. Sample menu: 45s work / 15s rest / 3 sets.

## 4. Tasks
| No | Item | Detail | Output |
|----|------|--------|--------|
| P-01 | Create project | `flutter create circuit_timer_poc`, add Riverpod. | Repo skeleton |
| P-02 | Timer core | Implement `TimerController` with 1s tick + tests. | Dart code + unit test |
| P-03 | Notification/vibration | Fire on phase transitions, schedule background notifications. | Working demo |
| P-04 | Background continuity | Android ForegroundService, iOS background task strategy. | Notes + code |
| P-05 | Accuracy check | Measure drift with stopwatch on device. | Log screenshot |
| P-06 | Retrospective | Summarize findings + required settings into docs. | Report |

## 5. Schedule
- Day 1: P-01 to P-03
- Day 2: P-04 to P-05, wrap-up with P-06

## 6. Success Criteria
- 3-set run without noticeable drift; measured error ≤ ±0.1s/min.
- Notifications/vibration fire on time in foreground/background.
- Backgrounding the app does not stop the timer.
- Risks and plugin requirements documented.

## 7. Risks & Mitigation
- No iOS device: use simulator logs first, schedule device test later.
- Android OEM optimizations: verify ForegroundService + battery whitelist.
- Plugin support: lock plugin versions compatible with Dart 3, fork if needed.

## 8. Next Steps
- Set up Flutter env and start P-01.
- Update this file and `mobile_timer_requirements.md` with PoC results.
\n## 9. 現状メモ (2025-12-14)\n- Flutter SDK 未導入のため PoC 実行前。\n- python/docs/flutter_setup.md にセットアップ手順を追加済み。\n- ドメイン層(lib/domain/)を Dart に移植済みなので、SDKインストール後はP-01=雛形生成を実行し、直ちにタイマー画面PoCへ着手可能。\n

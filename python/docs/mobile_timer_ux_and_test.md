# Mobile Timer UX Flow & Test Plan

Last Updated: 2025-12-09

## 1. Screen Flow (Textual Wireframe)
1. **Splash → Onboarding**: short intro, skip option. Leads to Home after acknowledging permissions (notifications/vibration).
2. **Home / Menu List**
   - Header: active day summary.
   - Menu cards: name, sets, work/rest summary, play button.
   - FAB: "New Menu".
   - Bottom nav: Home / History / Settings.
3. **Menu Detail Drawer** (from list tap)
   - Fields (read-only) + Edit button.
   - Primary CTA: Start timer.
4. **Menu Editor**
   - Inputs: name, work seconds, rest seconds, set count (steppers + preset chips).
   - Validation messages inline, Save button pinned bottom.
5. **Timer Screen**
   - Top: status text (Work/Rest, set X/Y).
   - Center: time remaining (large), radial progress.
   - Controls: Play/Pause toggle, Stop, Skip.
   - Footer: upcoming phase preview.
6. **History**
   - Date list grouped by day, show menu name + completion status.
   - Detail modal with session duration and notes.
7. **Settings**
   - Notification toggle, sound theme, vibration pattern, language selection.
   - Data section: Import/Export JSON, reset menus.

## 2. Interaction Notes
- Timer screen uses swipe-down to minimize into mini-player (persistent on Home).
- Critical notifications (phase changes) remain even if Do Not Disturb is on (user must allow "Time Sensitive" on iOS).
- When backgrounded, timer info appears in notification with remaining time + action buttons (Pause, Stop).

## 3. Test Plan Overview
### 3.1 Functional Tests
| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| T-F01 | Menu CRUD | Create → Edit → Delete menu | Data persists, validations trigger as defined |
| T-F02 | Timer basic flow | Start 3-set menu | Correct phase order, progress updates |
| T-F03 | Pause/Resume | Pause mid-phase, resume after 5s | Remaining time subtracts pause duration |
| T-F04 | Background notifications | Start timer → press Home → wait for next phase | Notification + vibration fire on time |
| T-F05 | Import/Export JSON | Export menus → clear → import | Data matches original file |

### 3.2 Non-Functional Tests
| ID | Scenario | Metric |
|----|----------|--------|
| T-N01 | Timer accuracy | Error ≤ ±0.1s/min measured vs stopwatch |
| T-N02 | App resume | App killed by OS → relaunch | Timer resumes or informs user to restart |
| T-N03 | Accessibility | Screen reader traversal | All controls labeled, focus order logical |
| T-N04 | Battery impact | 30 min continuous run | CPU < 20%, no abnormal drain |

### 3.3 Device Matrix (MVP)
| OS | Devices |
|----|---------|
| Android 13/14 | Pixel 5, Galaxy S22 |
| iOS 17 | iPhone 12, iPhone 15 |

## 4. Entry/Exit Criteria
- Entry: Flutter PoC (accuracy + notifications) completed, requirements signed off.
- Exit: All Must/Should test cases passed, no P1/P2 defects open.

## 5. Deliverables
- Test cases in spreadsheet or test management tool.
- Execution report per build (TestFlight/Internal App Sharing).
- Bug tickets referencing requirement IDs and test IDs.

## 6. Follow-ups
- Convert textual flow into Figma wireframes.
- Automate regression tests post-MVP (integration/UI tests).

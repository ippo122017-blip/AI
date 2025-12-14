import "training_menu.dart";

typedef PhaseCallback = void Function(Phase phase);
typedef TickCallback = void Function(Phase phase, int remaining, int elapsed);
typedef VoidCallback = void Function();

class TimerController {
  TimerController({
    this.onPhaseStart,
    this.onTick,
    this.onComplete,
  });

  final PhaseCallback? onPhaseStart;
  final TickCallback? onTick;
  final VoidCallback? onComplete;

  List<Phase> sequence = [];
  int totalSeconds = 0;
  int elapsedSeconds = 0;
  int currentIndex = 0;
  int remaining = 0;
  bool running = false;

  void loadMenu(TrainingMenu menu) {
    sequence = buildSequence(menu);
    totalSeconds = totalDuration(sequence);
    elapsedSeconds = 0;
    currentIndex = 0;
    remaining = sequence.isNotEmpty ? sequence.first.duration : 0;
    running = false;
  }

  void start() {
    if (sequence.isEmpty) {
      throw StateError('シーケンスが設定されていません');
    }
    elapsedSeconds = 0;
    currentIndex = 0;
    remaining = sequence.first.duration;
    running = true;
    _emitPhaseStart();
  }

  void stop() {
    running = false;
    elapsedSeconds = 0;
    remaining = 0;
    currentIndex = 0;
  }

  void tick([int seconds = 1]) {
    if (!running) return;
    remaining -= seconds;
    elapsedSeconds += seconds;
    if (remaining <= 0) {
      currentIndex += 1;
      if (currentIndex >= sequence.length) {
        running = false;
        onComplete?.call();
        return;
      }
      remaining = sequence[currentIndex].duration;
      _emitPhaseStart();
    }
    onTick?.call(sequence[currentIndex], remaining, elapsedSeconds);
  }

  Phase? get currentPhase =>
      (sequence.isEmpty || currentIndex >= sequence.length) ? null : sequence[currentIndex];

  void _emitPhaseStart() {
    if (sequence.isEmpty) return;
    onPhaseStart?.call(sequence[currentIndex]);
    onTick?.call(sequence[currentIndex], remaining, elapsedSeconds);
  }
}

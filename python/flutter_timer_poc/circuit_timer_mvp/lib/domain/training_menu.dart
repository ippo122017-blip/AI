class TrainingMenu {
  TrainingMenu({
    required this.name,
    required this.setSeconds,
    required this.restSeconds,
    required this.sets,
  });

  final String name;
  final int setSeconds;
  final int restSeconds;
  final int sets;

  factory TrainingMenu.fromJson(Map<String, dynamic> json) {
    return TrainingMenu(
      name: json['name'] as String,
      setSeconds: json['set_seconds'] as int,
      restSeconds: json['rest_seconds'] as int,
      sets: json['sets'] as int,
    );
  }

  Map<String, dynamic> toJson() => {
        'name': name,
        'set_seconds': setSeconds,
        'rest_seconds': restSeconds,
        'sets': sets,
      };
}

class Phase {
  Phase({
    required this.label,
    required this.duration,
    required this.setIndex,
    required this.totalSets,
  });

  final String label;
  final int duration;
  final int setIndex;
  final int totalSets;
}

List<Phase> buildSequence(TrainingMenu menu) {
  final phases = <Phase>[];
  for (var idx = 1; idx <= menu.sets; idx++) {
    phases.add(Phase(
      label: '作業',
      duration: menu.setSeconds,
      setIndex: idx,
      totalSets: menu.sets,
    ));
    if (idx < menu.sets && menu.restSeconds > 0) {
      phases.add(Phase(
        label: '休憩',
        duration: menu.restSeconds,
        setIndex: idx,
        totalSets: menu.sets,
      ));
    }
  }
  return phases;
}

int totalDuration(List<Phase> phases) =>
    phases.fold<int>(0, (acc, phase) => acc + phase.duration);

import json
from pathlib import Path

DATA_FILE = Path("workouts.json")


def load_workouts():
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError:
        return []


def save_workouts(workouts):
    DATA_FILE.write_text(json.dumps(workouts, indent=2))


def log_workout(exercise, sets, reps):
    return {
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
    }


# ✅ THIS MUST COME BEFORE THE LOOP
workouts = load_workouts()

print("Workout Logger")
print("Type 'done' when finished.\n")

while True:
    exercise = input("Exercise name: ").strip()
    if exercise.lower() == "done":
        break

    if not exercise:
        print("Please enter an exercise name.\n")
        continue

    try:
        sets = int(input("Sets: "))
        reps = int(input("Reps: "))
    except ValueError:
        print("Sets and reps must be numbers. Try again.\n")
        continue

    workouts.append(log_workout(exercise, sets, reps))
    print("Logged!\n")

save_workouts(workouts)

print("\nWorkout Summary (saved to workouts.json):")
for w in workouts:
    print(f"{w['exercise']}: {w['sets']} x {w['reps']}")

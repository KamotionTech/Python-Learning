import json
from datetime import date


DATA_FILE = "workouts.json"
LEGACY_SESSION_DATE = "Undated"


def prompt_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("\nInput ended. Exiting Workout Logger.")
        raise SystemExit(0)
    except KeyboardInterrupt:
        print("\nCancelled. Exiting Workout Logger.")
        raise SystemExit(0)


def save_sessions(sessions):
    with open(DATA_FILE, "w") as file:
        json.dump(sessions, file, indent=4)


def normalize_workout(entry):
    return {
        "exercise": entry.get("exercise", "Unknown exercise"),
        "sets": entry.get("sets"),
        "reps": entry.get("reps"),
        "weight": entry.get("weight"),
        "unit": entry.get("unit"),
    }


def normalize_session(entry):
    return {
        "date": entry.get("date", LEGACY_SESSION_DATE),
        "workouts": [normalize_workout(workout) for workout in entry.get("workouts", [])],
    }


def load_sessions():
    try:
        with open(DATA_FILE, "r") as file:
            raw_data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Could not read workouts.json because it is not valid JSON.")
        return []

    if not raw_data:
        return []

    if isinstance(raw_data, list) and "workouts" in raw_data[0]:
        return [normalize_session(entry) for entry in raw_data]

    legacy_workouts = [normalize_workout(entry) for entry in raw_data]
    return [{"date": LEGACY_SESSION_DATE, "workouts": legacy_workouts}]


def prompt_positive_int(label, default=None):
    prompt = f"{label}: " if default is None else f"{label} [{default}]: "

    while True:
        raw_value = prompt_input(prompt).strip()
        if raw_value == "" and default is not None:
            return default

        try:
            value = int(raw_value)
        except ValueError:
            print(f"Please enter a whole number for {label.lower()}.")
            continue

        if value <= 0:
            print(f"{label} must be greater than 0.")
            continue

        return value


def prompt_optional_weight(default=None):
    if default is None:
        prompt = "Weight (optional, press Enter to skip): "
    else:
        prompt = f"Weight (optional, press Enter to keep {default}): "

    while True:
        raw_value = prompt_input(prompt).strip()

        if raw_value == "":
            return default

        try:
            value = float(raw_value)
        except ValueError:
            print("Please enter a valid number for weight.")
            continue

        if value < 0:
            print("Weight cannot be negative.")
            continue

        return value


def prompt_optional_unit(weight, default=None):
    if weight is None:
        return None

    if default is None:
        prompt = "Unit (optional, lb/kg, press Enter to skip): "
    else:
        prompt = f"Unit (optional, lb/kg, press Enter to keep {default}): "

    while True:
        raw_value = prompt_input(prompt).strip().lower()

        if raw_value == "":
            return default

        if raw_value in ("lb", "kg"):
            return raw_value

        print("Please enter 'lb', 'kg', or press Enter to skip.")


def prompt_session_date(default=None):
    default = default or str(date.today())
    prompt = f"Session date (YYYY-MM-DD) [{default}]: "

    while True:
        raw_value = prompt_input(prompt).strip()
        if raw_value == "":
            return default

        try:
            return str(date.fromisoformat(raw_value))
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")


def build_workout_entry(existing=None):
    existing = existing or {}

    if existing:
        exercise_prompt = f"Exercise name [{existing['exercise']}]: "
    else:
        exercise_prompt = "Exercise name (or 'done' / 'undo'): "

    exercise = prompt_input(exercise_prompt).strip()

    if not existing:
        if exercise.lower() == "undo":
            return "undo"

        if exercise.lower() == "done":
            return "done"

    if exercise == "":
        if existing:
            exercise = existing["exercise"]
        else:
            print("Exercise name cannot be empty.")
            return None

    exercise = exercise.title()
    sets = prompt_positive_int("Sets", existing.get("sets"))
    reps = prompt_positive_int("Reps", existing.get("reps"))
    weight = prompt_optional_weight(existing.get("weight"))
    unit = prompt_optional_unit(weight, existing.get("unit"))

    return {
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weight": weight,
        "unit": unit,
    }


def get_or_create_session(sessions, session_date):
    for session in sessions:
        if session["date"] == session_date:
            return session

    session = {"date": session_date, "workouts": []}
    sessions.append(session)
    return session


def sort_sessions(sessions):
    def sort_key(session):
        session_date = session["date"]
        if session_date == LEGACY_SESSION_DATE:
            return (1, session_date)
        return (0, session_date)

    sessions.sort(key=sort_key)


def print_workout_summary(workouts):
    total_volume = 0

    if not workouts:
        print("No workouts logged yet.")
        return

    for i, entry in enumerate(workouts, start=1):
        exercise = entry["exercise"]
        sets = entry["sets"]
        reps = entry["reps"]
        weight = entry.get("weight")
        unit = entry.get("unit")
        volume = None

        if weight is not None:
            volume = sets * reps * weight
            total_volume += volume

        if weight is not None and unit is not None:
            print(
                f"{i}. {exercise}: {sets} sets x {reps} reps @ {weight} {unit} | Volume: {round(volume, 2)}"
            )
        elif weight is not None:
            print(
                f"{i}. {exercise}: {sets} sets x {reps} reps @ {weight} | Volume: {round(volume, 2)}"
            )
        else:
            print(f"{i}. {exercise}: {sets} sets x {reps} reps")

    if total_volume > 0:
        print(f"\nSession Total Volume: {round(total_volume, 2)}")


def print_all_sessions(sessions):
    print("\nWorkout Sessions:")

    if not sessions:
        print("No workouts logged yet.")
        return

    for index, session in enumerate(sessions, start=1):
        print(f"\n{index}. {session['date']}")
        print_workout_summary(session["workouts"])


def choose_session(sessions, action_name, allow_empty=False):
    if not sessions and not allow_empty:
        print(f"No sessions to {action_name}.")
        return None

    if sessions:
        print("\nSessions:")
        for index, session in enumerate(sessions, start=1):
            count = len(session["workouts"])
            label = "workout" if count == 1 else "workouts"
            print(f"{index}. {session['date']} ({count} {label})")

    choice = prompt_input(
        f"\nEnter session number to {action_name} (or press Enter to cancel): "
    ).strip()

    if choice == "":
        print("Cancelled.")
        return None

    try:
        session_number = int(choice)
    except ValueError:
        print("Please enter a valid number.")
        return None

    if session_number < 1 or session_number > len(sessions):
        print("That number is out of range.")
        return None

    return sessions[session_number - 1]


def choose_workout_number(workouts, action_name):
    if not workouts:
        print(f"No workouts to {action_name}.")
        return None

    print_workout_summary(workouts)
    choice = prompt_input(
        f"\nEnter workout number to {action_name} (or press Enter to cancel): "
    ).strip()

    if choice == "":
        print("Cancelled.")
        return None

    try:
        num = int(choice)
    except ValueError:
        print("Please enter a valid number.")
        return None

    if num < 1 or num > len(workouts):
        print("That number is out of range.")
        return None

    return num - 1


def delete_empty_session_if_needed(sessions, session):
    if not session["workouts"]:
        sessions.remove(session)


def delete_workout_by_number(sessions):
    session = choose_session(sessions, "delete from")
    if session is None:
        return

    print(f"\nSession: {session['date']}")
    index = choose_workout_number(session["workouts"], "delete")
    if index is None:
        return

    removed = session["workouts"].pop(index)
    delete_empty_session_if_needed(sessions, session)
    sort_sessions(sessions)
    save_sessions(sessions)
    print(f"Deleted: {removed.get('exercise', 'Unknown exercise')}")


def edit_workout_by_number(sessions):
    session = choose_session(sessions, "edit from")
    if session is None:
        return

    print(f"\nSession: {session['date']}")
    index = choose_workout_number(session["workouts"], "edit")
    if index is None:
        return

    current = session["workouts"][index]
    print("\nPress Enter to keep the current value.")
    updated = build_workout_entry(current)

    if updated is None:
        print("Edit cancelled.")
        return

    session["workouts"][index] = updated
    save_sessions(sessions)
    print(f"Updated: {updated['exercise']}")


def add_workout(sessions):
    default_date = str(date.today())
    session_date = prompt_session_date(default_date)
    session = get_or_create_session(sessions, session_date)

    print(
        f"\nAdd workouts for {session_date}. Type 'done' when finished or 'undo' to remove the last entry."
    )

    while True:
        entry = build_workout_entry()

        if entry == "done":
            break

        if entry == "undo":
            if session["workouts"]:
                removed = session["workouts"].pop()
                delete_empty_session_if_needed(sessions, session)
                sort_sessions(sessions)
                save_sessions(sessions)
                print(f"Removed last entry: {removed['exercise']}")
            else:
                print("Nothing to undo yet.")
            continue

        if entry is None:
            continue

        session = get_or_create_session(sessions, session_date)
        session["workouts"].append(entry)
        sort_sessions(sessions)
        save_sessions(sessions)
        print(f"Saved: {entry['exercise']}")


def print_menu():
    print("\nChoose an option:")
    print("1. Add workouts to a session")
    print("2. Edit a workout")
    print("3. Delete a workout")
    print("4. View all sessions")
    print("5. Quit")


def main():
    print("Workout Logger")
    sessions = load_sessions()
    sort_sessions(sessions)

    while True:
        print_menu()
        choice = prompt_input("Selection: ").strip()

        if choice == "1":
            add_workout(sessions)
        elif choice == "2":
            edit_workout_by_number(sessions)
        elif choice == "3":
            delete_workout_by_number(sessions)
        elif choice == "4":
            print_all_sessions(sessions)
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()

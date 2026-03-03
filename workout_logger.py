# List that stores all workout entries
# Each entry in the list is a dictionary
import json


print("Workout Logger")  # Print title so we know the script started
# Load existing workouts from file (persistent storage)


def save_workouts(workouts):
    with open("workouts.json", "w") as file:
        json.dump(workouts, file, indent=4)

def load_workouts():
    try:
        with open("workouts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def delete_workout_by_number(workouts):
    if not workouts:
        print("No workouts to delete.")
        return
    
    print_workout_summary(workouts)

    choice = input("\nEnter workout number to delete (or press Enter to cancel): ").strip()
    if choice == "":
        print("Cancelled.")
        return
    
    try:
        num = int(choice)
    except ValueError:
        print("Please enter a valid number.")
        return
    
    if num < 1 or num > len(workouts):
        print("That number is out of range.")
        return
    
    removed = workouts.pop(num - 1) # num-1 converts 1-based to 0-based index
    save_workouts(workouts)
    print(f"Deleted: {removed.get('exercise', 'Unknown exercise')}")

workouts = load_workouts()

def get_workout_entry():
    # This function asks the user for ONE workout entry
    # It returns a dictionary if the entry is valid
    # It returns None if input is invalid
    # It returns "done" if the user wants to stop

    exercise = input("Exercise name (or 'done' / 'undo'): ").strip()
    # Ask for exercise name and remove extra spaces from ends

    
    if exercise.lower() == "undo":
        return "undo"
    # Normalize input to lowercase so DONE, Done, done all become "done"

    if exercise.lower() == "done":
        return "done"  # Signal that user is finished

    if exercise == "":
        print("Exercise name cannot be empty.")
        return None  # Signal invalid input

    exercise = exercise.title()

    try:
        sets = int(input("Sets: "))
        # Convert sets input into an integer

        reps = int(input("Reps: "))
        # Convert reps input into an integer
    except ValueError:
        print("Please enter numbers only for sets and reps.")
        return None
        # Signal invalid input
    
    if sets <= 0 or reps <= 0:
        print("Sets and reps must be greater than 0.")
        return None
    
    weight = None
    unit = None
    # Default values so variables always exist

    weight_input = input("Weight (optional, press Enter to skip): ").strip()
    # Ask for optional weight

    if weight_input != "":
        try:
            weight = float(weight_input)
            # Convert weight to a number (float allows decimals)
        except ValueError:
            print("Invalid weight entered. Skipping weight.")
            weight = None
            # If conversion fails, ignore weight
    if weight is not None and weight < 0:
        print("Weight cannot be negative. Skipping weight.")
        weight = None

    unit_input = input("Unit (optional, lb/kg, press enter to skip,):").strip().lower()
    # Ask for optional unit and normalize it

    if unit_input == "":
        unit = None
        # No unit entered, store None
    elif unit_input in ("lb", "kg"):
        unit = unit_input
        # Store the unit if it is valid
    else:
        print("Invalid unit entered. Skipping unit.")
        unit = None
        # If unit is not lb or kg, ignore it


    entry = {
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weight": weight,
        "unit": unit,
    }
    # Create a dictionary that represents one workout entry

    return entry  # Send the dictionary back to the caller


def print_workout_summary(workouts):
    # This function prints all workout entries in a readable format

    print("\nWorkout Summary:")
    total_volume = 0
    # Print a header before listing workouts

    if not workouts:
        print("No workouts logged yet.")
        # Tell the user the list is empty
        return
        # Exit the function early so we don't run the loop below

    for i, entry in enumerate(workouts, start=1):
        # Loop through each workout dictionary in the list

        exercise = entry["exercise"]
        # Get the exercise name from the dictionary

        sets = entry["sets"]
        # Get the number of sets from the dictionary

        reps = entry["reps"]
        # Get the number of reps from the dictionary

        weight = entry.get("weight")
        # Get the weight from the dictionary

        unit = entry.get("unit")
        # Get the unit from the dictionary

        volume = None

        if weight is not None:
            volume = sets * reps * weight
            total_volume += volume
        # Total volume of lifts

        if weight is not None:
            # Only print weight if it exists

            if unit is not None:
                print(f"{i}. {exercise}: {sets} sets x {reps} reps @ {weight} {unit} | Volume: {round(volume, 2)}")
                # Print workout including weight and unit
            else:
                print(f"{i}. {exercise}: {sets} sets x {reps} reps @ {weight } | Volume: {round(volume, 2)}")
                # Print workout including weight but no unit
        else:
            print(f"{i}. {exercise}: {sets} sets x {reps} reps")
            # Print workout without weight
            
    if total_volume > 0:
        print(f"\nSession Total Volume: {round(total_volume, 2)}")

# Main loop: keep getting entries until user is done
while True:
    entry = get_workout_entry()
    # Ask the function for one workout entry

    if entry == "done":
        break
        # Stop looping if the function signals done

    if entry == "undo":
        if workouts:
            removed = workouts.pop()
            save_workouts(workouts)
            print(f"Removed last entry: {removed['exercise']}")
        else:
            print("Nothing to undo yet.")
        continue

    if entry is None:
        continue
        # Retry loop if input invalid

    workouts.append(entry)
    # Add the returned workout dictionary to the list
    save_workouts(workouts)

delete_workout_by_number(workouts)
print_workout_summary(workouts)
# Print the summary after the loop ends

save_workouts(workouts)
    

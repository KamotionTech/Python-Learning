# List that stores all workout entries
# Each entry in the list is a dictionary
workouts = []  # Create empty list to store workouts

print("Workout Logger")  # Print title so we know the script started


def get_workout_entry():
    # This function asks the user for ONE workout entry
    # It returns a dictionary if the entry is valid
    # It returns None if input is invalid
    # It returns "done" if the user wants to stop

    exercise = input("Exercise name (or 'done'): ").strip()
    # Ask for exercise name and remove extra spaces from ends

    exercise = exercise.lower()
    # Normalize input to lowercase so DONE, Done, done all become "done"

    if exercise == "done":
        return "done"  # Signal that user is finished

    if exercise == "":
        print("Exercise name cannot be empty.")
        return None  # Signal invalid input

    try:
        sets = int(input("Sets: "))
        # Convert sets input into an integer

        reps = int(input("Reps: "))
        # Convert reps input into an integer
    except ValueError:
        print("Please enter numbers only for sets and reps.")
        return None  # Signal invalid input

    entry = {
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
    }
    # Create a dictionary that represents one workout entry

    return entry  # Send the dictionary back to the caller


def print_workout_summary(workouts):
    # This function prints all workout entries in a readable format

    print("\nWorkout Summary:")
    # Print a header before listing workouts

    if not workouts:
        print("No workouts logged yet.")
        # Tell the user the list is empty
        return
        # Exit the function early so we don't run the loop below

    for entry in workouts:
        # Loop through each workout dictionary in the list

        exercise = entry["exercise"]
        # Get the exercise name from the dictionary

        sets = entry["sets"]
        # Get the number of sets from the dictionary

        reps = entry["reps"]
        # Get the number of reps from the dictionary

        print(f"{exercise}: {sets} sets x {reps} reps")
        # Print one formatted workout line


# Main loop: keep getting entries until user is done
while True:
    entry = get_workout_entry()
    # Ask the function for one workout entry

    if entry == "done":
        break
        # Stop looping if the function signals done

    if entry is None:
        continue
        # Retry loop if input invalid

    workouts.append(entry)
    # Add the returned workout dictionary to the list


print_workout_summary(workouts)
# Print the summary after the loop ends

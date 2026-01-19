#
# List, stores all workout entries.
# Per entry = dictionary

# Prints title
workouts = []
print("Workout Logger")

#Loop continues running until stopped with 'break'
while True:
# Ask use for exercise
# User input, returns string
    exercise = input("Exercise name (or 'done'): ").strip()
    # .strip() removes lead & trail spaces from user input
    exercise = exercise.lower()
    # .lower() converts strip to all lowercase characters
    # Allow us to compare input consistently throughout
    # DONE, Done, etc all become "done"

# If user enteres empty input
    if exercise == "":
        print("Exercise name cannot be empty.")
        continue

# If user types 'done', loop stops
# == means "is equal to"
    if exercise == "done":
        break # exit loop
#
    try:
        sets = int(input("Sets: ")) # Convert user input into number (int)
        reps = int(input("Reps: "))

# Tell user what went wrong
# Continue skip loop iteration and retry
    except ValueError:
        print("Please enter numbers only for sets and reps.")
        continue

# Create dictionary to group related data
# One dicitonary = one workout entry
    entry = {
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
    }

# Add dictionary to workout list
# Append puts it at end of list
    workouts.append(entry)

def print_workout_summary(workouts):
    # This function prints all workout entries in a readable format
    
    print("\nWorkout Summary:")
    # Print a header before listing workouts

    for entry in workouts:
        # Loop through each wokrout dictionary in the list

        exercise = entry["exercise"]
        # Get the exercise name from dictionary

        sets = entry["sets"]
        # Get the number of sets

        reps = entry["reps"]
        # Get the number of reps

        print(f"{exercise}: {sets} sets x {reps} reps")
        # Print one formatted workout line

print_workout_summary(workouts)
        # Call the function and pass in the workouts list



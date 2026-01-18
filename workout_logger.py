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

# Print summary of workouts after loop is done
# \n adds a blank line before the text
print("\nWorkout Summary:")

# Loop through each wokrout entry in the list
for entry in workouts:
    # Access valeus in the dictionary using their keys
    exercise = entry["exercise"]
    sets = entry["sets"]
    reps = entry["reps"]

    # Print one workout in a readable format
    print(f"{exercise}: {sets} sets x {reps} reps")


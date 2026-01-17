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
    exercise = input("Exercise name (or 'done'): ")

# If user types 'done', loop stops
# == means "is equal to"

    if exercise == "done":
        break # exit loop

# User input sets
sets = int(input("Sets "))

# User input reps
reps = int(input("Reps: "))


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

# Print all workouts after loop is done
print(workouts)


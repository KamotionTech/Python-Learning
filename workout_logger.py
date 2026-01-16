#

workouts = []
print("Workout Logger")

#
exercise = input("Exercise name: ")
sets = int(input("Sets "))
reps = int(input("Reps: "))

entry = {
    "exercise": exercise,
    "sets": sets,
    "reps": reps,
}

workouts.append(entry)
print(workouts)


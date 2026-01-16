#Variables
name = "Kam"
age = 29
height_cm = 171.5
is_learning_python = True

print(name)
print(age)
print(height_cm)
print(is_learning_python)

#Math
next_year_age = age + 1
height_m = height_cm / 100

print("Next year age:", next_year_age)
print("Height in meters:", height_m)

def greet(name):
    return f"Hello, {name}!"

message = greet(name)
print(message)

workouts = ["Pull", "Push", "Legs"]

for workout in workouts:
    print("Workout day:", workout)

name = input("What is your name? ")
age = int(input("How old are you? "))

if age >= 18:
    print(f"Welcome, {name}. You're an adult.")
else:
    print(f"Hey {name}, you're under 18.")
    
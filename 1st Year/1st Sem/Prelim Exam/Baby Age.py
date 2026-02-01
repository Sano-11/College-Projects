cody_age = int(input("Enter age of The Programmer: "))
teacher_age = int(input("Enter age of his teacher: "))
peter_age = int(input("Enter age of his friend, Peter: "))

baby_age = ((cody_age * teacher_age) / (peter_age))+1

print(f"Baby's age = {baby_age:.0f}")
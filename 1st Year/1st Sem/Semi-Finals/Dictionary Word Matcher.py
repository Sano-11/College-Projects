words = input("Enter dictionary words separated by space: \n").split()

target = input("Enter target word: \n")

sortedtarget = sorted(target)
matching = [word for word in words if sorted(word) == sortedtarget]


print("Matching words:", ", ".join(matching))
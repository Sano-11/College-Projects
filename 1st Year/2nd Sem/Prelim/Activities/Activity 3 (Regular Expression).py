import re

# Getting the content from the user via input
file_path = input("Enter the file path: ")

# Open and read the file (not using 'with')
data_file = open(file_path,)
data = data_file.read() 
data_file.close()

print()

# Lines na nag sstart w/ Python
python_lines = re.findall('^Python.*', data, re.MULTILINE)
for line in python_lines:
    print(line)

# Numbewr Extractor
num_strings = re.findall('[0-9]+', data)
numbers = [int(n) for n in num_strings]

# Computation
total_sum = sum(numbers)
highest_num = max(numbers) if numbers else 0

# Vowel Counter
vowels = re.findall('[aeiouAEIOU]', data, re.IGNORECASE)
vowel_total = len(vowels)

# Python Word Counter ito
python_word_matches = re.findall('Python', data)
python_count = len(python_word_matches)

# --- OUTPUT ---
print(f"\nThe sum of all numbers is {total_sum}")
print(f"The highest number is {highest_num}")
print(f"The total vowel count is {vowel_total}")
print(f"Python word count is {python_count}\n")
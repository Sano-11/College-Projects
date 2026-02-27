import csv, os
 
# Get the directory where the script is located
script_dir = os.path.dirname(__file__) 

# Combine that directory with the filename
filename = os.path.join(script_dir, "census.csv")

# Dictionary
city_counts = {}              # {state: number_of_cities}
state_pop = {}         # {state: total_state_population}
highest_city = {}             # {state: (city, population)}
lowest_city = {}              # {state: (city, population)}

# CSV Reader
with open(filename, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
 
    for row in reader:
        state = row["STNAME"].strip()
        city = row["CTYNAME"].strip()
        population = int(row["CENSUS2010POP"])
 
        # Capture state total population 
        if state == city:
            state_pop[state] = population
            continue  # Skip counting as a city
 
        # Count total cities per state 
        if state not in city_counts:
            city_counts[state] = 0
        city_counts[state] += 1
 
        # Highest population city per state
        if state not in highest_city or population > highest_city[state][1]:
            highest_city[state] = (city, population)
 
        # Lowest population city per state
        if state not in lowest_city or population < lowest_city[state][1]:
            lowest_city[state] = (city, population)

# Total Cities / State

print("\nTotal Cities per State:\n")
for state, count in city_counts.items():
    print(f"- {state}: ({count})")

# Highestt

highest_state = max(city_counts, key=city_counts.get)
print("\nState with Highest Number of Cities:\n")
print(f"- {highest_state}: ({city_counts[highest_state]})")

# Lowest

low_state = min(city_counts, key=city_counts.get)
print("\nState with Lowest Number of Cities:\n")
print(f"- {low_state}: ({city_counts[low_state]})")

# Total 2010 census population / state

print("\nTotal 2010 Population per State:\n")
for state, pop in state_pop.items():
    print(f"- {state}: ({pop})")

# City / state with highest 2010 population

print("\nCity per State with Highest 2010 Population:\n")
for state, (city, pop) in highest_city.items():
    print(f"- {state}: {city} ({pop})")

# City / state with lowest 2010 population

print("\nCity per State with Lowest 2010 Population:\n")
for state, (city, pop) in lowest_city.items():
    print(f"- {state}: {city} ({pop})")
 
# Export
output_file = os.path.join(script_dir, "US2010Census.csv")
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["State", "Total Cities", "Total 2010 Population\n"])
 
    for state in city_counts:
        writer.writerow([state, city_counts[state], state_pop.get(state, 0)])
 
print("\nUS2010Census.csv file has been created successfully.")
import pandas as pd
import os

# --- PATH LOGIC ---
# This ensures the script looks for the CSV in the same folder as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "suicide.csv")

# Load the data
df = pd.read_csv(file_path)

# ## Activity 1 (Country, Year, Age, Sex, Suicide)
print("--- Activity 1 ---")
print(df[['country', 'year', 'sex', 'age', 'suicides/100k pop']])

# ## Activity 2 & 3 Suicide record (Philippines 2011)
print("\n--- Activity 2 & 3: Philippines Records ---")
ph_records = df[df['country'] == 'Philippines']
ph_2011 = ph_records[ph_records['year'] == 2011]
print(ph_2011[['year', 'sex', 'age', 'suicides_no', 'suicides/100k pop']])

# ## Activity 4 Highest suicide per 100k population in 2005
print("\n--- Activity 4: Highest Suicide Rate in 2005 ---")
highest_2005 = df[df['year'] == 2005].sort_values(by='suicides/100k pop', ascending=False).head(1)
print(highest_2005[['country', 'year', 'sex', 'age', 'suicides/100k pop']])

# ## Activity 5 Stats per Year
print("\n--- Activity 5: Year Stats (Descending) ---")
year_stats = df.groupby('year').agg({'suicides_no': 'sum', 'suicides/100k pop': 'sum'})
print(year_stats.sort_values(by='suicides_no', ascending=False))

# ## Activity 6 Stats per Gender
print("\n--- Activity 6: Gender Stats ---")
gender_stats = df.groupby('sex').agg({'suicides_no': 'sum', 'suicides/100k pop': 'sum'})
print(gender_stats.sort_values(by='suicides_no', ascending=False))

# ## Activity 7 Stats per Age
print("\n--- Activity 7: Age Stats ---")
age_stats = df.groupby('age').agg({'suicides_no': 'sum', 'suicides/100k pop': 'sum'})
print(age_stats.sort_values(by='suicides_no', ascending=False))

# ## Activity 8 Total cases per Country and Year
print("\n--- Activity 8: Country/Year Stats ---")
country_year_stats = df.groupby(['country', 'year'])[['suicides_no']].sum()
print(country_year_stats.sort_values(by='suicides_no', ascending=False).head(10))

# ## Activity 9 Total cases in Philippines (Year, Gender, Age)
print("\n--- Activity 9: Detailed Philippines Stats ---")
ph_total_stats = df[df['country'] == 'Philippines'].groupby(['year', 'sex', 'age'])[['suicides_no']].sum()
print(ph_total_stats)

# ## Activity 10 Year with highest cases in Philippines
print("\n--- Activity 10: Philippines Peak Year ---")
ph_highest_year = df[df['country'] == 'Philippines'].groupby('year')[['suicides_no']].sum()
print(ph_highest_year.sort_values(by='suicides_no', ascending=False).head(1))
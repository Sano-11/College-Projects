startyr = int(input("Enter the start year: "))
endyr = int(input("Enter the end year: "))

for year in range(startyr, endyr+1):
    if not ((year %4 ==0 and year%100!=0) or (year %400 ==0)):
        continue

    print(year,end=" ")
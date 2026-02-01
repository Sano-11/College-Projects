mdict = {
    "fruit": ["banana", "apple","orange"],
    "vegetable": ["carrot", "celery","broccoli"],
    "meat": ["chicken", "beef","pork"],
}

key = input("Enter a key to search for: ").lower()

if key in mdict:
    sort = sorted(mdict[key])
    print(f"Values associated with key '{key}' in alphabetical order: ")
    for item in sort:
        print(item)
else:
    print(f"Key '{key}' not found in dictionary.")
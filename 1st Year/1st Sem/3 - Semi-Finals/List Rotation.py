nums = list(map(int, input("Enter the list of integers separated by space: ").split()))

rota = int(input("Enter the number of positions to rotate to the right: "))

rota = rota % len(nums)
rotatedlist = nums[-rota:] + nums[:-rota]
print(rotatedlist)
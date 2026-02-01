money = int(input("Enter the initial amount of money: "))
interest = float(input("Enter the interest in percent: "))

new_interest = interest * 0.01
new_money = money + (money * new_interest)

print(f"The new amount of money is {new_money:.2f}")
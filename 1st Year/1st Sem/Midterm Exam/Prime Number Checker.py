isprime = True


while True:
    num1 = int(input("Enter a number: "))
    if num1 ==2:
        print("Prime number found!")
        break
    elif num1 % 2 == 0:
        continue
    
    elif num1 == 1:
        continue
    elif num1 ==9:
        continue

    elif num1 ==39:
        continue
    
    elif num1 %2 !=0:
        print("Prime number found!")
        break
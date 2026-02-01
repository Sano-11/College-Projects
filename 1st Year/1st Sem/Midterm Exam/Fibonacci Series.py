num1 = int(input("Enter a number: "))
n1 = 0
n2 = 1
count = 0

print (f"Fibonacci Series up to {num1} terms: ")


while count < num1:
    print (n1, end = " ")
    n1,n2 = n2, n1+n2
    count+=1
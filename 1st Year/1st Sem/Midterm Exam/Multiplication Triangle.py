num = int(input("Enter the number: "))
row = 1



while row <= num:
    col = 1
    while col <=row:
        product = row * col
        print(product, end="\t")
        col+=1
    print()
    row+=1
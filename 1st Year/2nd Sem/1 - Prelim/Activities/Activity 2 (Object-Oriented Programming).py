class Loan:
    def __init__(self, loan_type, amount):
        self.loan_type = loan_type
        self.amount = amount

class Employee:
    def __init__(self):
        self.__name = ""
        self.__gender = ""
        self.__bdate = ""
        self.__position = ""
        self.__rate = 0.0
        self.__dayswork = 0
        self.__loan = []

    # Setter and Getter
    @property
    def name(self): return self.__name
    @name.setter
    def name(self, value): self.__name = value
        
    @property
    def gender(self): return self.__gender
    @gender.setter
    def gender(self, value): self.__gender = value

    @property
    def bdate(self): return self.__bdate
    @bdate.setter
    def bdate(self, value): self.__bdate = value

    @property
    def position(self): return self.__position
    @position.setter
    def position(self, value): self.__position = value

    @property
    def rate(self): return self.__rate
    @rate.setter
    def rate(self, value): self.__rate = value

    @property
    def dayswork(self): return self.__dayswork
    @dayswork.setter
    def dayswork(self, value): self.__dayswork = value


    def getGross(self):
        return self.__dayswork * self.__rate

    def getSSS(self):
        gross = self.getGross()
        if 500 <= gross < 10000:
            return 500.0
        elif 10000 <= gross <= 20000:
            return 1000.0
        else:
            return 1500.0

    def getTax(self):
        gross = self.getGross()
        if gross < 10000:
            return 0.0
        elif 10000 <= gross < 20000:
            return gross * 0.10
        elif 20000 <= gross <= 30000:
            return gross * 0.20
        else:
            return gross * 0.25
        
    # Loan Looper to
    def getLoan(self):
        
        userchoice = input("\nAny loan [Y/N]? ").upper()
        if userchoice == 'Y':
            while True:
                l_type = input("Type: ")
                l_amount = float(input("Amount: "))
                self.__loan.append(Loan(l_type, l_amount))
                
                cont = input(f"\nAccept another loan [Y/N]? ").upper()
                if cont == 'N':
                    break

    def getTotalLoan(self):
        total = 0
        for item in self.__loan:
            total += item.amount
        return total

    def getNetSalary(self):
        return self.getGross() - self.getSSS() - self.getTax() - self.getTotalLoan()

    def getEmployeeDetails(self):
        print("\nEmployee Details:\n")
        print(f"Name: {self.name}")
        print(f"Gender: {self.gender}")
        print(f"Birth Date: {self.bdate}")
        print(f"Position: {self.position}")

    def displayLoanDetails(self):
        print("\nLoan Details:\n")
        for item in self.__loan:
            print(f"{item.loan_type} P {item.amount:,.2f}")

# Main
def main():
    emp = Employee()
    
    # setters gamit
    emp.name = input("Enter Employee Name: ")
    emp.gender = input("Enter Gender (M/F): ")
    emp.bdate = input("Enter Birth Date: ")
    emp.position = input("Enter Position: ")
    emp.rate = float(input("Enter Rate per day: "))
    emp.dayswork = int(input("Enter Days Worked: "))
    
    emp.getLoan()
    
    emp.getEmployeeDetails()
    emp.displayLoanDetails()
    
    print("\nSalary Details:\n")
    print(f"Gross Salary: P {emp.getGross():,.2f}")
    print(f"SSS: P {emp.getSSS():,.2f}")
    print(f"Tax: P {emp.getTax():,.2f}")
    print(f"Total Loan: P {emp.getTotalLoan():,.2f}")
    print(f"Net Salary: P {emp.getNetSalary():,.2f}")

if __name__ == "__main__":
    main()
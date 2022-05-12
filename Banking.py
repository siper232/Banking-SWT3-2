import math

maxLoanAmount = 10000.00
maxLoans = 3
minBalance = 50.00
maxTransfer = 5000

interestRate = 0.05  # 5%
startInterestLoan = 0.1  # 10%
maxAdaptation = 0.005  # 0.5%
loanMaxMonths = 12
currentLoanInterest = startInterestLoan

totalMoney = 0

homeLogin = ["help", "login", "signup", "exit"]
loginCommands = ["help", "home", "signup", "exit"]
signupCommands = ["help", "home", "login", "exit"]
loggedInCommands = ["help", "logout", "checkAccount", "createLoan",
                    "makeDeposit", "makeLoanDeposit", "makeWithdrawal", "exit"]
transactionCommands = ["help", "cancel", "exit"]

clientsInfo = []

user = ""
userIdx = None

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = float(round(balance, 2))
        self.loans = []
        self.locked = False

    def makeDeposit(self, deposit):
        self.balance = float(round(self.balance + deposit, 2))
        if self.balance > 0:
            self.locked = False

    def makeWithdrawal(self, withdraw):
        self.balance = float(round(self.balance - withdraw, 2))
        if self.balance <= 0:
            self.locked = True

    def makeLoanDeposit(self, idx, deposit):
        self.loans[idx].makeDeposit(deposit)
        self.balance = float(round(self.balance - deposit, 2))
        if self.loans[idx].amount == 0:
            self.loans.pop(idx)

    def addMonth(self):
        anyOvertime = False
        makeWithdrawal(self.balance * (1 - interestRate))
        for idx, loan in enumerate(self.loans):
            self.loans[idx].addMonth()
            if self.loans[idx].time > loanMaxMonths:
                anyOvertime = True
            if self.loans[idx].time > loanMaxMonths + 1:
                makeLoanDeposit(idx, self.loans[idx].amount)
        self.locked = anyOvertime


class Loan:
    def __init__(self, amount):
        self.amount = float(round(amount, 2))
        self.time = 0  # in months

    def makeDeposit(self, deposit):
        self.amount -= float(round(deposit, 2))

    def addMonth(self):
        self.time += 1

        if self.time <= loanMaxMonths:
            self.amount = float(round(self.amount * currentLoanInterest, 2))


def welcome():
    global user

    print("\n\n\nWelcome to the bank of fuck you, we give no fucks :)\n\n")
    print("For a list of all commands at any point type \"help\".\n")

    while True:
        command = input(
            "Please choose whether to \"login\" or to \"signup\".\n")
        if command == "help":
            possibleCommands(homeLogin)
        elif command == "exit":
            exit()
        elif command == "login":
            login()
        elif command == "signup":
            signup()
        else:
            print("Command was not accepted, please try again.\n")


def login():
    global user
    global userIdx
    global totalMoney

    succeeded = False
    clientNames = [client.name for client in clientsInfo]

    print("\n\nWelcome to fuck you bank login.\n")

    while not succeeded:
        command = input("Please provide your username to log in.\n")

        if command == "help":
            possibleCommands(loginCommands)
        elif command == "exit":
            exit()
        elif command == "home":
            print("Returning to home.\n\n")
            welcome()
        elif command in clientNames:
            user = command
            userIdx = clientNames.index(command)
            succeeded = True
        else:
            print(
                "Username/command does not exist, please try again or type \"help\" for possible commands.\n")
    loggedIn()


def signup():
    global user

    usernameSucceeded = False
    accountSucceeded = False
    clientNames = [client.name for client in clientsInfo]

    print("\n\nWelcome to fuck you bank signup\n")

    while not usernameSucceeded:
        command = input("Please insert your username\n")
        if command == "help":
            possibleCommands(signupCommands)
        elif command == "exit":
            exit()
        elif command == "home":
            print("Returning to home.\n\n")
            welcome()
        elif " " in command:
            print("Username can only be one word.\n")
        elif command in clientNames:
            print("Username already exists, please use another one.\n")
        else:
            usernameSucceeded = True
            user = command

    while not accountSucceeded:
        command = input("Please insert your balance\n")
        if command == "help":
            possibleCommands(signupCommands)
        elif command == "exit":
            exit()
        elif command == "home":
            print("returning to home\n\n")
            welcome()
        else:
            if correctMoney(command):
                if float(command) < minBalance:
                    print("Account cannot be created with a balance below " +
                          str(minBalance) + " euros.\nPlease try again\n")
                else:
                    makeAccount(user, float(command))
                    totalMoney += float(command)
                    accountSucceeded = True

    print("You have successfully created your account. You will be redirected to the home page.\n")
    welcome()


def loggedIn():
    global user
    global userIdx

    online = True

    print("\n\nWelcome " + user + ", to the fuck you bank.\n\n")
    while online:
        command = input("How can we help you today?\n")
        if command == "help":
            possibleCommands(loggedInCommands)
        elif command == "exit":
            exit()
        elif command == "logout":
            user = ""
            userIdx = None
            online = False
            welcome()
        elif command == "checkAccount":
            showAccount()
        elif command == "createLoan":
            newLoan()
        elif command == "makeDeposit":
            makeDeposit()
        elif command == "makeLoanDeposit":
            makeLoanDeposit()
        elif command == "makeWithdrawal":
            makeWithdrawal()
        elif command == "skipMonth":
            skipMonth()
        else:
            print(
                "Command does not exist, please try again or type \"help\" for possible commands.\n")


def newLoan():
    global clientsInfo

    completed = False

    if clientsInfo[userIdx].locked:
        print("Your account has been locked due to not fully paying a loan within " +
              str(loanMaxMonths) + " months.")
    elif len(clientsInfo[userIdx].loans) == maxLoans:
        print("You can not get a new loan. You already have " +
              str(maxLoans) + " loans.")
    else:
        while not completed:
            command = input("How much money would you like to lend?\n")
            if command == "help":
                possibleCommands(transactionCommands)
            elif command == "cancel":
                completed = True
            elif command == "exit":
                exit()
            else:
                if correctMoney(command):
                    if float(command) < maxLoanAmount:
                        newLoan = Loan(float(command))
                        clientsInfo[userIdx].loans.append(newLoan)
                        clientsInfo[userIdx].makeDeposit(float(command))
                        print("Your new loan has been created with an amount of " +
                              str(float(command)) + " euros\n")
                        completed = True
                    else:
                        print("The max amount of a loan is " + str(maxLoanAmount) +
                              " euros. Please input a number below this amount.")


def makeDeposit():
    global totalMoney
    global currentLoanInterest

    completed = False

    while not completed:
        command = input(
            "How much money would you like to put into your account?\n")
        if command == "help":
            possibleCommands(transactionCommands)
        elif command == "cancel":
            completed = True
        elif command == "exit":
            exit()
        else:
            if correctMoney(command):
                if float(command) <= maxTransfer and float(command) > 0:
                    clientsInfo[userIdx].makeDeposit(float(command))
                    print("You have successfully deposited " +
                        str(float(command)) + " euros\n")
                    totalMoney += float(command)
                    if currentLoanInterest < 1:
                        currentLoanInterest = round(startInterestLoan + (maxAdaptation * math.floor(totalMoney / maxTransfer)), 3)
                    completed = True
                else:
                    print("You can only make a deposit of max " + str(maxTransfer) + " euros and cannot be smaller than 1 euro\nPlease try again\n")


def makeLoanDeposit():
    completed = False
    completed2 = False

    showAccount()

    if clientsInfo[userIdx].locked:
        print("Your account has been locked and payment will be done automatically each month.")
    else:
        while not completed:
            command = input(
                "What loan would you like to make a deposit on? (look at the number before the loans, example: 1)\n")
            if command == "help":
                possibleCommands(transactionCommands)
            elif command == "cancel":
                completed = True
            elif command == "exit":
                exit()
            else:
                try:
                    index = int(command)
                    if index <= len(clientsInfo[userIdx].loans) and index > 0:
                        loanIdx = index - 1
                        completed = True
                        print("")

                        while not completed2:
                            command = input(
                                "How much money would you like to deposit from your account to the selected loan?\n")
                            if command == "help":
                                possibleCommands(transactionCommands)
                            elif command == "cancel":
                                completed2 = True
                            elif command == "exit":
                                exit()
                            else:
                                if correctMoney(command):
                                    if float(command) <= clientsInfo[userIdx].balance and float(command) > 0:
                                        if float(command) <= clientsInfo[userIdx].loans[loanIdx].amount:
                                            clientsInfo[userIdx].makeLoanDeposit(
                                                loanIdx, float(command))
                                            print("You have successfully deposited " + str(
                                                float(command)) + " euro to loan number " + str(index) + "\n")
                                            completed2 = True
                                        else:
                                            print(
                                                "You can't deposit more money than needed to pay off your loan.\n")
                                    else:
                                        print(
                                            "You don't have enough money in your balance to pay this amount or your deposit is less than 1 euro.\n")
                    else:
                        print("This loan does not exist, please try again.\n")
                except ValueError:
                    print(
                        "Please provide a full number like 1, 2 or 3 to select your loan.\n")


def makeWithdrawal():
    global totalMoney
    global currentLoanInterest

    completed = False
    if clientsInfo[userIdx].locked:
        print("Your account has been locked and payment will be done automatically each month.")
    else:
        while not completed:
            command = input(
                "How much money would you like to retrieve from your account?\n")
            if command == "help":
                possibleCommands(transactionCommands)
            elif command == "cancel":
                completed = True
            elif command == "exit":
                exit()
            else:
                if correctMoney(command):
                    if clientsInfo[userIdx].balance >= float(command) and float(command) > 0:
                        if float(command) <= maxTransfer:
                            clientsInfo[userIdx].makeWithdrawal(float(command))
                            print("You have successfully withdrawn " +
                                str(float(command)) + " euros\n")
                            totalMoney -= float(command)
                            if currentLoanInterest > 0:
                                currentLoanInterest = round(startInterestLoan + (maxAdaptation * math.floor(totalMoney / maxTransfer)), 3)
                            completed = True
                        else:
                            print("You can only make a withdraw of max " + str(maxTransfer) + " euros\nPlease try again\n")
                    else:
                        print(
                            "You do not have the balance to withdraw this amount of money and can only withdraw more than 1 euro, please input a different amount or type \"cancel\"")


def showAccount():
    client = clientsInfo[userIdx]
    print("\nName: " + client.name + "\nBalance: {:.2f} euro\nLoans:".format(client.balance))
    print("\tAmount\t\tCurrent interest\tLoan next month\t\tMonths to pay off")
    for idx, loan in enumerate(client.loans):
        print(str(idx + 1) + "\t{:.2f} euro\t{:.1f}%\t\t\t{:.2f} euro\t\t{:n} month(s)".format(loan.amount, currentLoanInterest*100, round(loan.amount + (loan.amount * currentLoanInterest), 2), loanMaxMonths - loan.time))
    print("")


def makeAccount(username, balance):
    global totalMoney

    newClient = Account(username, balance)
    clientsInfo.append(newClient)
    totalMoney += balance


def skipMonth():
    print("Skipping month for every user registered\n")
    for client in clientsInfo:
        client.addMonth()


def possibleCommands(commands):
    print("Possible commands:")
    for command in commands:
        print("\t" + command)
    print("")


def exit():
    print("\n\nExitting program, have a nice day :)")
    quit()


def correctMoney(amount):
    try:
        money = int(amount)
        money = float(amount)
        if money > 0:
            return True
        else:
            print("Your amount can only be above 0 euros.\nPlease try again\n")
            return False

    except ValueError:

        try:
            values = amount.split(".")

            if len(values) == 2:
                euros = int(values[0])
                cents = int(values[1])

                if len(values[1]) <= 2:

                    money = float(amount)

                    if money > 0:
                        return True
                    else:
                        print("Your amount can only be above 0 euros.\nPlease try again\n")
                        return False

                else:
                    print(
                        "Please enter a valid amount consisting of no more than 2 numbers after the \".\"\nPlease try again\n")
                    return False
            else:
                print("Please enter a valid amount consisting of full euros or with a decimal value seperated by a single \".\"\nPlease try again\n")
                return False
        except ValueError:
            print("Please provide a correct amount consisting of only numbers or numbers with a decimal value seperated by a \".\"\nPlease try again\n")
            return False


if __name__ == "__main__":
    welcome()

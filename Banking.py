# clientInfo = {
#   Max: {
#     balance: 5000,
#     loan: 200,
#     currentInterest: 50,
#   },
#   John: {
#     balance: 2000,
#     loan: 0,
#     currentInterest: 0,
#   },
#   Nobody: {
#     balance: 6000,
#     loan: 100,
#     currentInterest: 70,
#   },
# }

class Accounts:
  def __init__(self, name, balance, loan):
    self.name = name
    self.balance = balance
    self.loan = loan

noRightsCommands = ["help", "login", "signup"]
normalUserRights = ["help", "logout", "exit"]
adminUserRIghts = ["help", "logout", "exit"]

interest = 0.1

command = ""
user = ""


def welcome():
  succeeded = False

  print("Welcome to the bank of fuck you, we give no fucks :)\n\n")
  print("For a list of all commands at any point type \"help\"\n")

  while not succeeded:
    command = input("Please choose whether to \"login\" or to \"signup\"\n")
    if command == "help":
      print("Possible commands:\n\tlogin\n\tsignup\n\n")
    elif command == "exit":
      quit()
    elif command != "login" and command != "signup":
      print("Command was not accepted, please try again\n")
    elif command == "login":
      succeeded = True
      login()
    elif command == "signup":
      signup()
    else:
      print("Unknown error, please try again\n")


def login():
  succeeded = False

  print("Welcome to the fuck you bank login\n")

  while not succeeded:
    command = input("Please provide your username\n")

    if command == "help":
      print("Possible commands:\n\t...\n")
    elif command == "exit":
      quit()
    elif command == "home":
      print("returning to home\n\n")
      welcome()
    elif clientInfo.has_key(command):
      user = command
    else:
      print("Username/command does not exist, please try again or type \"exit\" to exit")


def signup():
  usernameSucceeded = False
  accountSucceeded = False

  print("Welcome to fuck you bank signup\n")

  while not usernameSucceeded:
    command = input("Please insert your username\n")
    if command == "help":
      print("Possible commands:\n\t...\n")
    elif command == "exit":
      quit()
    elif " " in command:
      print("Username can only be one word\n")
    elif clientInfo.has_key(command):
      print("Username already exists, please use another one\n")
    else:
      usernameSucceeded = True
      user = command

  while not accountSucceeded:
    command = input("Please insert your balance\n")
    if command == "help":
      print("Possible commands:\n\t...\n")
    elif not command.isnumeric():
      print("Balance can only consist of numbers\n")
    else:
      accountSucceeded = True
      # clientInfo[user] = {
      #   balance = int(command),
      #   interest: 0,
      # }


def loggedIn():
  print("Welcome " + user + " to the fuck you bank.\n\n")
  command = input("How can we help you today?")
  if command == "help":
    print("Possible commands:\n\t...\n")
  elif command == "exit":
    quit()
  else:
    print("Something went wrong, please try again")


# while user == "":
#     command = input("Please provide your name to sign in.\n")
#     if (command in clientInfo):
#         user = command
#         print("Welcome " + user + " to the bank of fuck you")
#     elif command == "exit":
#         print("Exiting login\n\n")
#     else:
#         print("Username does not exist, please try again or type \"exit\" to exit")

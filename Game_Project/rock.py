from random import randint
t = ["rock","paper","scissor"]
computer = t[randint(0,2)]
player = False
while player == False:
    player = input("rock,paper,scissor?")
    if player == computer:
        print("TIE!")
    elif player == "rock":
        if computer == "paper":
            print("Computer Wins")
        else:
            print("YOU WINS")
    elif player == "paper":
        if computer == "rock":
            print("YOU WINS")
        else:
            print("Computer Wins")
    elif player == "scissor":
        if computer == "paper":
            print("YOU WINS")
        else:
            print("Computer Wins")
    else:
        print("INVALID PLAY")
    player == False
    computer = t[randint(0,2)]
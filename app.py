import random, sys, model
from game import run_game




from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["todo_db"]
characters = db["characters"]
monsters = db["monsters"]


while(True):
    print(model.menu())
    choice = input("Enter your choice (number): ")
    match choice:
        case "1":
            print("Game started!")
            run_game()
        case "2":
            name = input("Enter character name: ")
            hp = int(input("Enter character HP: "))
            attack = int(input("Enter character Attack: "))
            char_id = add_character(name, hp, attack)
            print(f"Character added with ID: {char_id}")
        case "3":
            name = input("Enter monster name: ")
            hp = int(input("Enter monster HP: "))
            attack = int(input("Enter monster Attack: "))
            race = input("Enter monster race: ")
            mon_id = add_monster(name, hp, attack, race)
            print(f"Monster added with ID: {mon_id}")
        case "4":
            print(model.list_characters())
        case "5":
            print(model.list_monsters())
        case "6":
            print("Exiting the game. Goodbye!")
            client.close()
            break
        

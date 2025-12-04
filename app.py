from classes import Monster
import random, sys, model
from game import run_game
from model import add_character_to_db, add_monster_to_db, list_characters, list_monsters, get_characters 
from data import load_data

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["todo_db"]
characters = db["characters"]
monsters = db["monsters"]


while(True):
    load_data()
    print(model.menu())
    choice = input("Enter your choice (number): ")
    match choice:
        case "1":
            print("Game started!")  
            run_game()
        case "2":
            print("High Scores:")
            high_scores = db["high_scores"]
            for score in high_scores.find().sort("score", -1).limit(10):
                print(f"Player: {score['player_name']}, Score: {score['score']}")
        case "3":
            name = input("Enter character name: ")
            hp = int(input("Enter character HP: "))
            attack = int(input("Enter character Attack: "))
            defense = float(input("Enter character Defense: "))
            char_id = add_character_to_db(name, hp, attack, defense)
            new_character = model.Character(name, hp, attack, defense)
            print(f"Character added with ID: {char_id}")
        case "4":
            name = input("Enter monster name: ")
            hp = int(input("Enter monster HP: "))
            attack = int(input("Enter monster Attack: "))
            defense = float(input("Enter monster Defense: ")) 
            race = input("Enter monster race: ")
            mon_id = add_monster_to_db(name, hp, attack, defense, race)
            new_monster = Monster(name, hp, attack, defense, race)
            print(f"Monster added with ID: {mon_id}")
        case "5":
            print(model.list_characters())
            print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        case "6":
            print(model.list_monsters())
            print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        case "7":
            print("Exiting the game. Goodbye!")
            client.close()
            break
        

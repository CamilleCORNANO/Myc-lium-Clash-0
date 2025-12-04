from hashlib import new
from pymongo import MongoClient
from classes import Character, Monster
import data

client = MongoClient("mongodb://localhost:27017")
db = client["Mycelium_Clash"]
db_characters = db["characters"]
db_monsters = db["monsters"]

def menu():
    MAIN_MENU = """
    1. Play Game
    2. High Scores
    3. Add Character
    4. Add Monster
    5. List Characters
    6. List Monsters
    7. Exit
    """
    return MAIN_MENU   

def add_character_to_db(name, hp, attack, defense):
    new_character = {
        "Name": name,
        "HP": hp,
        "Attack": attack,
        "Defense": defense
    }
    insert_character = db_characters.insert_one(new_character)
    return insert_character.inserted_id

def add_monster_to_db(name, hp, attack, defense, race):
    new_monster = {
        "Name": name,
        "HP": hp,
        "Attack": attack,
        "Defense": defense,
        "Race": race
    }
    insert_monster = db_monsters.insert_one(new_monster)
    return insert_monster.inserted_id

def add_score_to_db(player):
    new_score = {
        "PlayerName": player.name,
        "Score": player.get_score(),
        "Team" : player.team_state()
        }    
    insert_score = db["high_scores"].insert_one(new_score)
    return insert_score.inserted_id


def list_characters():
    characters = get_characters()[0]
    for character in characters:
        print(character)
    
        
def list_monsters():
    monsters = get_characters()[1]
    for monster in monsters:
        print(monster)
        
def get_characters():
    characters = []
    monsters = []
    for character in db_characters.find():
        new_character = Character(
            character["Name"],
            character["HP"],
            character["Attack"],
            character["Defense"]
        )
        characters.append(new_character)  
    for monster in db_monsters.find():
        new_monster = Monster(
            monster["Name"],
            monster["HP"],
            monster["Attack"],
            monster["Defense"],
            monster["Race"]
        )
        monsters.append(new_monster)
    return characters, monsters

"""def get_character_by_name(name):
    character = db_characters.find_one({"Name": name})
    if character:
        return Character(
            character["Name"],
            character["HP"],
            character["Attack"],
            character["Defense"]
        )
    return None"""


def clear_database():
    db_characters.delete_many({})
    db_monsters.delete_many({})

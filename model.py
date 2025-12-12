from hashlib import new
from pymongo import MongoClient
from classes import Character, Monster, Skill, Special
import data

client = MongoClient("mongodb://localhost:27017")
db = client["Mycelium_Clash"]
db_characters = db["characters"]
db_monsters = db["monsters"]
db_high_scores = db["high_scores"]
db_skills = db["skills"]
db_specials = db["specials"]

def menu():
    MAIN_MENU = """
    1. Play Game
    2. High Scores
    3. Add Character
    4. Add Monster
    5. List Characters
    6. List Monsters
    7. List Skills and Specials
    8. Exit
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
    
def list_skills():
    skills = get_skills()
    for skill in skills:
        print(skill)

def list_specials():
    specials = db_specials.find()
    for special in specials:
        print(special)

        
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
    
def get_skills():
    skills = []
    specials = []
    for skill in db_skills.find():
        new_skill = Skill(
            skill["Name"], 
            skill["Power"], 
            skill["Trigger"], 
            skill["Description"]
        )
        skills.append(new_skill)
    for special in db_specials.find():
        new_special = Special(
            special["Name"], 
            special["Power"], 
            special["Trigger"], 
            special["User"],
            special["Description"],
        )
        specials.append(new_special)
    return skills, specials

def load_high_scores():
    high_scores = db_high_scores.find().sort("Score", -1).limit(10)
    for idx, score_entry in enumerate(high_scores, 1):
        print(f"{idx}. {score_entry['PlayerName']} - Score: {score_entry['Score']} - Team: {', '.join(score_entry['Team'])}")

def get_by_name(name):
        characters, monsters = get_characters()
        skills, specials = get_skills()
        for character in characters:
            if character.name == name:
                return character
        for monster in monsters:
            if monster.name == name:
                return monster
        for skill in skills:
            if skill.name == name:
                return skill
        for special in specials:
            if special.name == special:
                return special
        print(f"No {name} not found.")
        return None

def clear_database(unit):
    match unit:
        case "characters":
            db_characters.delete_many({})
        
        case "monsters":
            db_monsters.delete_many({})
        
        case "high_scores":
            db_high_scores.delete_many({})
        
        case "skills":
            db_skills.delete_many({})
        
        case "specials":
            db_specials.delete_many({})
        
        case "all":
            db_characters.delete_many({})
            db_monsters.delete_many({})
            db_high_scores.delete_many({})
            db_skills.delete_many({})
            db_specials.delete_many({})
        
        case _:  # Le _ est le "default" (comme else)
            print("Invalid unit specified.")
            return  # Sort de la fonction sans afficher le message de succès
    
    print(f"Cleared all data from {unit} collection.")

clear_database("all")
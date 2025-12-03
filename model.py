from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["Mycelium_Clash"]
characters = db["characters"]
monsters = db["monsters"]

class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.health = hp
        self.attack = attack
        self.defense = defense
    def is_alive(self):
        return self.health > 0
    def take_damage(self, damage):
        self.health -= damage
    def deal_damage(self, other):
        other.take_damage(self.attack)
        
class Monster(Character):
    def __init__(self, name, hp, attack, race, defense):
        super().__init__(name, hp, attack, defense)
        self.race = race
       

class Player():
    def __init__(self, name):
        self.name = name
        self.characters = []
        self.score = 0
    def add_character(self, character):
        self.characters.append(character)
    def get_characters(self):
        return self.characters
    def get_score(self):
        return self.score
    def increase_score(self):
        self.score += 1
class Team():
    def __init__(self):
        self.members = []
    def add_member(self, character):
        if len(self.members) < 3 and character not in self.members:
            self.members.append(character)
    def get_members(self):
        return self.members    

def menu():
    MAIN_MENU = """
    1. Play Game
    2. Add Character
    3. Add Monster
    4. List Characters
    5. List Monsters
    6. Exit
    """
    print(MAIN_MENU)


    

def add_character(name, hp, attack):
    new_character = {
        "Name": name,
        "HP": hp,
        "Attack": attack
    }
    insert_character = characters.insert_one(new_character)
    return insert_character.inserted_id

def add_monster(name, hp, attack, race):
    new_monster = {
        "Name": name,
        "HP": hp,
        "Attack": attack,
        "Type": race
    }
    insert_monster = monsters.insert_one(new_monster)
    return insert_monster.inserted_id

def list_characters():
    for character in characters.find():
        print(character)
        
def list_monsters():
    for monster in monsters.find():
        print(monster)
def clear_database():
    characters.delete_many({})
    monsters.delete_many({})

client.close()
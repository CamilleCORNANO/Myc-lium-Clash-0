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
    def get_character(self):
        return {
            "Name": self.name,
            "HP": self.health,
            "Attack": self.attack,
            "Defense": self.defense
        }
        
class Monster(Character):
    def __init__(self, name, hp, attack, defense, race):
        super().__init__(name, hp, attack, defense)
        self.race = race      
    def get_character(self):
        base_character = super().get_character()
        base_character["Race"] = self.race
        return base_character
    def get_character(self):
        return {
            "Name": self.name,
            "HP": self.health,
            "Attack": self.attack,
            "Defense": self.defense,
            "Race": self.race
        }

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
    2. High Scores
    3. Add Character
    4. Add Monster
    5. List Characters
    6. List Monsters
    7. Exit
    """
    return MAIN_MENU   

def add_character(name, hp, attack, defense):
    new_character = {
        "Name": name,
        "HP": hp,
        "Attack": attack,
        "Defense": defense
    }
    insert_character = characters.insert_one(new_character)
    return insert_character.inserted_id

def add_monster(name, hp, attack, defense, race):
    new_monster = {
        "Name": name,
        "HP": hp,
        "Attack": attack,
        "Defense": defense,
        "Type": race
    }
    insert_monster = monsters.insert_one(new_monster)
    return insert_monster.inserted_id

def list_characters():
    for character in characters.find():
        print(character.get_character())
        
def list_monsters():
    for monster in monsters.find():
        print(monster.get_character())
        
def get_characters():
    for character in characters.find():
        new_character = Character(
            character["Name"],
            character["HP"],
            character["Attack"],
            character["Defense"]
        )
    for monster in monsters.find():
        new_monster = Monster(
            monster["Name"],
            monster["HP"],
            monster["Attack"],
            monster["Type"],
            monster["Defense"],
            monster["Race"]
        )
    return list(characters.find())

def get_character_by_name(name):
    character = characters.find_one({"Name": name})
    if character:
        return Character(
            character["Name"],
            character["HP"],
            character["Attack"],
            character["Defense"]
        )
    return None

def clear_database():
    characters.delete_many({})
    monsters.delete_many({})


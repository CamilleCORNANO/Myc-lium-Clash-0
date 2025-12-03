from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["Mycelium_Clash"]
db_characters = db["characters"]
db_monsters = db["monsters"]

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
    def __str__(self):
        return f"{self.name} (HP: {self.health}, Attack: {self.attack}, Defense: {self.defense})"

    def __add__(self, other):
        if isinstance(other, Character):
            return Character(
                name=f"{self.name}-{other.name}",
                hp=self.health + other.health,
                attack=self.attack + other.attack,
                defense=self.defense + other.defense
            )
        return NotImplemented
    
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
    def __str__(self):
        return f"{self.name} (HP: {self.health}, Attack: {self.attack}, Defense: {self.defense}, Race: {self.race})"

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
    insert_character = db_characters.insert_one(new_character)
    return insert_character.inserted_id

def add_monster(name, hp, attack, defense, race):
    new_monster = {
        "Name": name,
        "HP": hp,
        "Attack": attack,
        "Defense": defense,
        "Race": race
    }
    insert_monster = db_monsters.insert_one(new_monster)
    return insert_monster.inserted_id

def list_characters():
    characters = get_characters()[0]
    print(characters)
    for character in characters:
        return character.get_character()
    
        
def list_monsters():
    monsters = get_characters()[1]
    print(monsters)
    for monster in monsters:
        return monster.get_character()
        
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

def get_character_by_name(name):
    character = db_characters.find_one({"Name": name})
    if character:
        return Character(
            character["Name"],
            character["HP"],
            character["Attack"],
            character["Defense"]
        )
    return None

def clear_database():
    db_characters.delete_many({})
    db_monsters.delete_many({})

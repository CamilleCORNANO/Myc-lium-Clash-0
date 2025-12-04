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
        if self.health <= 0:
            self.health = 0
            print(f"{self.name} has been defeated!")
    
    def get_character(self):
        return {
            "Name": self.name,
            "HP": self.health,
            "Attack": self.attack,
            "Defense": self.defense
        }
    def __str__(self):
        return f"{self.name} \n (HP: {self.health}, Attack: {self.attack}, Defense: {self.defense})"

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
        return f"{self.name} \n (HP: {self.health},  Attack: {self.attack}, Defense: {self.defense}, Race: {self.race})"
class Player():
    def __init__(self, name):
        self.name = name
        self.characters = Team()
        self.score = Score()
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
    def alive_members(self):
        return [member for member in self.members if member.is_alive()]
    def is_defeated(self):
        return all(not member.is_alive() for member in self.members)

class Score():
    def __init__(self):
        self.value = 0
    def increase(self, amount=1):
        self.value += amount
    def get_value(self):
        return self.value
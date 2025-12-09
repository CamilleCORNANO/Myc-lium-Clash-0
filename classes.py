import random
class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.health = hp
        self.attack = attack
        self.defense = defense
        self.killer = None
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health -= damage * self.defense
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
    def return_killer(self):
        return f"Killed by {self.killer}"
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
        self.score = Score(self)
    def add_character_to_team(self, character):
        self.characters.add_member(character)
    def get_characters(self):
        return self.characters
    def get_score(self):
        return self.score.get_score()
    def increase_score(self):
        self.score.increase()
    def team_state(self):
        team_display = []
        for member in self.get_characters().get_members():
            if member.is_alive():
                team_display.append(member.name)
            else:
                team_display.append(f"{member.name} (Dead, {member.return_killer()})")
        return team_display
        
class Team():
    def __init__(self):
        self.members = []
    def add_member(self, character):
        self.members.append(character)
    def get_members(self):
        return self.members
    def alive_members(self):
        return [member for member in self.members if member.is_alive()]
    def is_defeated(self):
        return all(not member.is_alive() for member in self.members)

class Score():
    def __init__(self, player):
        self.value = 0
        self.player = player.name
        self.team = player.get_characters()
    def __str__(self):
        return f"Player: {self.player}, Score: {self.value}"
    def increase(self, amount=1):
        self.value += amount
    def get_score(self):
        return self.value
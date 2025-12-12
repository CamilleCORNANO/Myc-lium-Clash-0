import random
import time

from game import skills

class Character:
    def __init__(self, name, hp, attack, defense, luck, skills):
        self.name = name
        self.health = hp
        self.attack = attack
        self.defense = defense
        self.luck = luck
        self.skills = skills
        self.killer = None
    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health -= damage * self.defense
        if self.health <= 0:
            self.health = 0
            print(f"{self.name} has been defeated!")
    def luck_roll(self):
        return self.luck * 1,3
    
    def __str__(self):
        return f"{self.name} \n (HP: {self.health}, Attack: {self.attack}, Defense: {self.defense})"
    def return_killer(self):
        return f"Killed by {self.killer}"
    
    def use_skills(self, team, foes):
        for s in self.skills:
            skills(s.name, self, team, foes)
            
    
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
    def get_team(self):
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
    
class Skill:
    def __init__(self, name, power, trigger, description):
        self.name = name
        self.power = power
        self.trigger = trigger
        self.description = description
    def __str__(self):
        return f"{self.name} (Power: {self.power}, Trigger: {self.trigger}) - {self.description} /n"
    
    def trigger_okay(self, luck):
        trigger = self.trigger + luck
        if trigger < 1:
            return False
        if trigger > 1 :
            if self.trigger_okay(trigger) :
                
            return True

class Special(Skill):
    def __init__(self, name, power, trigger, user, description):
        super().__init__(name, power, trigger, description)
        self.user = user
    def __str__(self):
        return f"{self.name} (User: {self.user}, Power: {self.power}, Trigger: {self.trigger}) - {self.description} /n"
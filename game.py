from random import random
from model import *

def run_game():
    while True:
        print("Running the game... (Press 'q' to quit)")
        command = input("Enter command: ")
        if command.lower() == 'q':
            print("Exiting game loop.")
            break
        else:
            print(f"Command '{command}' not recognized. Try again.")

def battle(player_team, monster_team):
    player_team = player_team
    monster_team = random.choice(get_characters()[1])
    print("Battle started between player team and monster team!")
    while not player_team.is_defeated() and not monster_team.is_defeated():
        turn(player_team, monster_team)
        if monster_team.is_defeated():
            print("Players win the battle!")
            break
        turn(monster_team, player_team)
        if player_team.is_defeated():
            print("Monsters win the battle!")
            break
        
def turn(team, foes):
    while team.alive_members():
        alive = team.alive_members()
        for member in alive:
                print(f"{member.name} attacks!")
                attack(member, random.choice(foes.alive_members()))
        
def attack(attacker, defender):
    damage = attacker.attack * random.uniform(0.8, 1.2)
    defender.take_damage(damage)
    print(f"{attacker.name} deals {damage:.0f} damage to {defender.name}!")
    #.0f formats the damage to 0 decimal places
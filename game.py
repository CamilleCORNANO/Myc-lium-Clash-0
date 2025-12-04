import random
from model import *
from classes import Player, Team, Character, Monster
from utils import get_int_input
from data import load_data

def run_game():
    while True:
        print("Running the game... (Press 'q' to quit)")
        command = input("Enter command: ")
        if command.lower() == 'q':
            print("Exiting game loop.")
            break
        else:
            player = create_player()
            while len(player.characters.get_members()) < 3:
                selected_character = character_select()
                player.characters.add_member(selected_character)
                print(f"Player {player.name} has selected the following characters: {', '.join([member.name for member in player.characters.get_members()])}")
            player_team = player.get_characters()
            num_monsters = 1
            battle(player_team, num_monsters)
            num_monsters = increase_monsters(player.get_score().score, num_monsters)
            if player.get_score().score >= 5:
                print(f"Congratulations {player.name}, you have won the game!")
                game_over(player)
                high_scores = db["high_scores"]
                high_scores.insert_one({"player_name": player.name, "score": player.get_score().score})
                break
            
        
def create_player():
    player_name = input("Enter your player name: ")
    player = Player(player_name)
    print(f"Welcome, {player.name}!")
    return player

def character_select():
    characters, _ = get_characters()
    print("SELECT YOUR CHARACTERS")
    print("Available Characters:")
    for idx, character in enumerate(characters):
        print(f"{idx + 1}. {character.name}")
    player_choice = get_int_input("Enter the number of the character you want to select: ") - 1
    if player_choice < 0 or player_choice >= len(characters):
        print("Invalid choice. Please try again.")
        return character_select()
    selected_character = characters[player_choice]
    print(f"You selected: {selected_character.name} !")
    return selected_character

def score_update(player):
    player.get_score().increase_score() 
    print(f"{player.name}'s score increased to {player.get_score().score}!")
    
def game_over(player):
    print("Game Over! Thanks for playing.")
    add_score_to_db(player, player.get_score().score)
    return player.get_score()
    
def increase_monsters(score, num_monsters):
    if score % 2 != 0:
        num_monsters += 1
    return num_monsters

def start_battle(num_monsters):
    _ , monsters = get_characters()
    selected_monsters = random.sample(monsters, num_monsters)
    monster_team = Team()
    for monster in selected_monsters:
        monster_team.add_member(monster)
    monster_names = ", ".join([f"{i}. {monster.name}" for i, monster in enumerate(monster_team.members, 1)])
    print(f"Battle started between player team and {monster_names}!")
    return monster_team

def battle(player_team, num_monsters):
    monster_team = start_battle(num_monsters)
    while not player_team.is_defeated() and not monster_team.is_defeated():
        turn(player_team, monster_team)
        if monster_team.is_defeated():
            print("Players win the battle!")
            score_update(player_team)
            break
        turn(monster_team, player_team)
        if player_team.is_defeated():
            print("Monsters win the battle!")
            game_over()
            break

def turn(team, foes):
    alive = team.alive_members()
    for member in alive:
        if not foes.alive_members():
            break
        print(f"{member.name} attacks!")
        attack(member, random.choice(foes.alive_members()))
        
def attack(attacker, defender):
    damage = attacker.attack * random.uniform(0.8, 1.2)
    defender.take_damage(damage)
    print(f"{attacker.name} deals {damage:.0f} damage to {defender.name}!")
    #.0f formats the damage to 0 decimal places
    
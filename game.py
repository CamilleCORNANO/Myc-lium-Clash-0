import random
import time
from model import *
from classes import Player, Team, Character, Monster
from utils import get_int_input, get_by_name, get_characters, 

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
            print(player.get_characters())
            level = level(player.get_score)
            battle(player, level)
            #num_monsters = increase_monsters(player.get_score(), num_monsters)
            if player.get_score() >= 5:
                print(f"Congratulations {player.name}, you have won the game!")
                game_over(player)
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
    add_score_to_db(player)
    return player.get_score()

    
def level(level):
    match level:
        case 1:
            selected_monsters = [get_by_name("anti-Wokes"), 
                                 get_character_by_name("Tonton raciste"), 
                                 get_character_by_name("Bobo parisien"),
                                 get_character_by_name("Bonapartiste")] 
            return create_monster_team(selected_monsters, 1)
        case 2:
            selected_monsters = [get_by_name("Flic"), 
                                 get_character_by_name("La CRIF"), 
                                 get_character_by_name("Emmanuel Macron")] 
            return create_team(selected_monsters)
        case 3:
            selected_monsters = [get_character_by_name("Les services de renseignement"), 
                                 get_character_by_name("Le nationalisme"),
                                 get_character_by_name("Le consumérisme"), 
                                 get_character_by_name("Le grand déni des crimes de guerres Japonais"),
                                 get_character_by_name("L'Hégémonie Culturelle Etatsunienne")
                                 ]
            return create_monster_team(selected_monsters, 1)
        case 4:
            selected_monsters = [get_character_by_name("Le Patriarcat"), 
                                 get_character_by_name("Le grand Capital"), 
                                 get_character_by_name("Les lobbys agro-industriels"),
                                 get_character_by_name("Le lobby pharmaceutique"),
                                 ]
            return create_monster_team(selected_monsters, 2)
        case 5:
            selected_monsters = [get_character_by_name("Le Réchauffement Climatique")]
            return create_team(selected_monsters)
        case _:
            print("argument level incorrect")
            return None

def create_monster_team(monster_names_list, num_monsters):
    monster_team = Team()
    
    for _ in range(num_monsters):
        # Sélectionne un monstre aléatoire dans la liste
        selected_names = random.sample(monster_names_list, min(num_monsters, len(monster_names_list)))
        monster = get_character_by_name(random.choice(selected_names))
        
        if monster:  # Vérification que le monstre existe
            monster_team.add_member(monster)
    return monster_team

def create_team(names_list):
    new_team = Team()
    for name in names_list:
        character = get_character_by_name(name)
        if character:
           new_team.add_member(character)
    return new_team
    
  
def battle(player, score):
    monster_team = level(score)
    while not player.get_team().is_defeated() and not monster_team.is_defeated():
        turn(player.get_team(), monster_team)
        if monster_team.is_defeated():
            print("Players win the battle!")
            score_update(player)
            break
        turn(monster_team, player.get_characters())
        if player.get_team().is_defeated():
            print("Monsters win the battle!")
            game_over(player)
            break

def turn(team, foes):
    combat_pause(type_pause="turn_start", team_name=", "
                    .join([member.name for member in team.get_members()]))
    alive = team.alive_members()
    for member in alive:
        if not foes.alive_members():
            break
        print(f"{member.name} attacks!")
        attack(member, random.choice(foes.alive_members()))
        member.use_skills(member, foes, team)
        
def attack(attacker, defender):
    damage = attacker.attack * random.uniform(0.8, 1.2)
    damage = crit_chance(damage)
    defender.take_damage(damage)
    print(f"{attacker.name} deals {damage:.0f} damage to {defender.name}!")
    combat_pause(type_pause="damage", damage=damage, defender_name=defender.name)
    if not defender.is_alive():
        print(f"{attacker.name} has defeated {defender.name}!")
        combat_pause(type_pause="defeat", defender_name=defender.name)
        defender.killer = attacker.name
    #.0f formats the damage to 0 decimal places
    
def combat_pause(type_pause, **kwargs):
    match type_pause:
        case "action":
            attacker = kwargs.get('attacker_name', 'Attaquant')
            # Animation de préparation
            print(f"{attacker} ", end="", flush=True)
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.3)
            print(" ATTAQUE !")
            time.sleep(0.5)
        
        case "damage":
            damage = kwargs.get('damage', 0)
            defender = kwargs.get('defender_name', 'Cible')
            # Affichage des dégâts avec emphase
            print(f"{defender} subit {damage:.0f} points de dégâts !")
            time.sleep(1.5)
        
        case "defeat":
            defender = kwargs.get('defender_name', 'Ennemi')
            # Animation de défaite
            print(f"\n{'='*50}")
            print(f"{defender} a été vaincu !")
            print(f"{'='*50}")
            time.sleep(2.5)
        
        case "turn_start":
            team_name = kwargs.get('team_name', 'Équipe')
            print(f"\n{'='*50}")
            print(f"Tour de : {team_name}")
            print(f"{'='*50}")
            time.sleep(1)
        
        case "turn_end":
            print(f"\n{'-'*50}")
            time.sleep(1)
        
        case "critical":
            # Pause spéciale pour un coup critique
            print(" COUP CRITIQUE !")
            time.sleep(1)
        
        case _:
            # Cas par défaut
            print("Type de pause inconnu")

def crit_chance(character, damage):
    luck_multiplier = character.luck_roll()
    crit_threshold = 0.1 * luck_multiplier
    if random.random() < crit_threshold:
        print("Critical Hit!")
        combat_pause(type_pause="critical")
        return damage * 3
    return damage
    
def skills(skill_name, user, team, foes):
    match skill_name:
        case "Slash":
            slash(user, foes)
        case "Fire":
            print(f"Using skill: {skill_name}!")
            time.sleep(1)
        case "Heal":
            heal(user, team)
            print(f"Using skill: {skill_name}!")
            time.sleep(1)
        case "Ice":
            print(f"Using skill: {skill_name}!")
            time.sleep(1)
        case "Thunder":
            print(f"Using skill: {skill_name}!")
            time.sleep(1)
    print(f"Using skill: {skill_name}!")
    time.sleep(1)


    
def slash(foes, user):
    
    target = random.choice(foes)
    slash = get_by_name("Slash")
    if slash.trigger(user.luck_roll()) == True :
        damage = (user.attack * slash.power / 10) * random.uniform(0.8, 1.2)
        print(f"{user} uses Slash !")
        time.sleep(1)
        
        return damage
    
    
    
def heal(team):
    return
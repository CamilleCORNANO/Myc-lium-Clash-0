import random
import time
from model import *
from classes import Player, Team, Character, Monster
from utils import get_int_input, get_by_name, get_characters

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
            level = next_level(player.get_score)
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

    
def next_level(level):
    match level:
        case 1:
            selected_monsters = [get_by_name("anti-Wokes"), 
                                 get_by_name("Tonton raciste"), 
                                 get_by_name("Bobo parisien"),
                                 get_by_name("Bonapartiste")] 
            return create_monster_team(selected_monsters, 1)
        case 2:
            selected_monsters = [get_by_name("Flic"), 
                                 get_by_name("La CRIF"), 
                                 get_by_name("Emmanuel Macron")] 
            return create_team(selected_monsters)
        case 3:
            selected_monsters = [get_by_name("Les services de renseignement"), 
                                 get_by_name("Le nationalisme"),
                                 get_by_name("Le consumérisme"), 
                                 get_by_name("Le grand déni des crimes de guerres Japonais"),
                                 get_by_name("L'Hégémonie Culturelle Etatsunienne")
                                 ]
            return create_monster_team(selected_monsters, 1)
        case 4:
            selected_monsters = [get_by_name("Le Patriarcat"), 
                                 get_by_name("Le grand Capital"), 
                                 get_by_name("Les lobbys agro-industriels"),
                                 get_by_name("Le lobby pharmaceutique"),
                                 ]
            return create_monster_team(selected_monsters, 2)
        case 5:
            selected_monsters = [get_by_name("Le Réchauffement Climatique")]
            return create_team(selected_monsters)
        case _:
            print("argument level incorrect")
            return None

def create_monster_team(monster_names_list, num_monsters):
    monster_team = Team()
    
    for _ in range(num_monsters):
        # Sélectionne un monstre aléatoire dans la liste
        selected_names = random.sample(monster_names_list, min(num_monsters, len(monster_names_list)))
        monster = get_by_name(random.choice(selected_names))
        
        if monster:  # Vérification que le monstre existe
            monster_team.add_member(monster)
    return monster_team

def create_team(names_list):
    new_team = Team()
    for name in names_list:
        character = get_by_name(name)
        if character:
           new_team.add_member(character)
    return new_team
    
  
def battle(player, monster_team):
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
    if defender.defeat(attacker) :
        combat_pause(type_pause="defeat")
    #.0f formats the damage to 0 decimal places


def combat_pause(type_pause, **kwargs):
    match type_pause:
        case "action":
            for _ in range(3):
                print(".", end="", flush=True)
                time.sleep(0.3)
            time.sleep(0.5)
        
        case "damage":
            time.sleep(1.5)
        
        case "one hit ko":
            time.sleep(1.4)
        
        case "heal":
            time.sleep(1)
        
        case "defeat":
            # Animation de défaite
            print(f"\n{'='*50}")
            print(f"{'='*50}")
            time.sleep(2.5)
        
        case "turn_start":
            print(f"\n{'='*50}")
            print(f"Début de tour.")
            print(f"{'='*50}")
            time.sleep(1)
        
        case "turn_end":
            print(f"\n{'-'*50}")
            print("Fin de tour.")
            print(f"\n{'-'*50}")
            time.sleep(1)
        
        case "critical":
            print(" COUP CRITIQUE !")
            time.sleep(1)
        
        case "mort subite":
            print("MORT SUBITE !!")
            time.sleep(1.3)
        case "special" :
            print("CAPACITE SPECIALE ACTIVEE.")
            time.sleep(2)
            
            
        
        case _:
            # Cas par défaut
            print("Type de pause inconnu")

def crit_chance(character, damage, coeff=0.2):
    luck_multiplier = character.luck_roll()
    crit_threshold = coeff * luck_multiplier
    if random.random() < crit_threshold:
        print("Critical Hit!")
        combat_pause(type_pause="critical")
        return damage * 3
    return damage
    
def skills(skill_name, user, team, foes):
    match skill_name:
        case "Slash":
            slash(user, foes)
        case "Slam":
            slam(user, foes)
        case "Smash":
            smash(user, foes)
        case "Shot":
            shot(user, foes)
        case "Heal":
            heal(user, team)
        case "Panacea":
            user.take_damage(recoil(panacea(user, team), 0.1))
        case "Fire":
            fire(user, foes)
        case "Ice":
            ice(user, foes)
        case "Thunder":
            thunder(user, team, foes)
        case "Earthquake":
            earthquake(user, foes)
        case "Wind":
            wind(user, foes)
        case "Water":
            water(user, team, foes)
        case "Light":
            light(user, team, foes)
        case "Darkness":
            darkness(user, team, foes)
        case "Void":
            void(user, team, foes)
        case "Hellfire":
            hellfire(user, team, foes)
        case "Sophisme":
            sophisme(user, team, foes)
        case "Appel Regie":
            appel_regie(user, team, foes)
        case "To Ashes":
            to_ashes(user, team, foes)
        case "Pacify":
            pacify(user, team, foes)
        case "Inferno":
            inferno(user, team, foes)
        case "Tsunami":
            tsunami(user, team, foes)
        case "Blizzard":
            blizzard(user, team, foes)
        case "Meteor Geyser":
            meteor_geyser(user, team, foes)
        case "Moon":
            moon(user, team, foes)
        case "Sun":
            sun(user, team, foes)
        case "Unforgettable Kind":
            unforgettable_kind(user, team, foes)
        case "Peppy Parade":
            peppy_parade(user, team, foes)
        case "The Sin of Envy":
            the_sin_of_envy(user, team, foes)
        case _:
            print(f"Skill {skill_name} not implemented yet!")



    
def generic_SU(foes, user, skill_name):
    target = random.choice(foes.alive_members())
    skill = get_by_name(skill_name)
    num_attacks = skill.trigger_okay(user.luck_roll())
    damages = []
    if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
        for _ in range(num_attacks):  # Plus pythonic que while
            damage = (user.attack * skill.power / 10) * random.uniform(0.8, 1.2)
            if damage >= user.attack :
                damage *= 3 #critique garanti
            else:
                damage = crit_chance(user, damage)
            damages.append(damage) #pour Recoil()
            print(f"{user.name} uses {skill_name} on {target.name}! {target.name} takes {damage} damage !")
            num_attacks -= 1
            combat_pause(type_pause="action", attacker_name=user.name)
            target.take_damage(damage)
            combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
            if target.is_defeated():
                target.defeat()
            target = random.choice(foes.alive_members())
    return damages

def generic_AOE(foes, user, skill_name):
    skill = get_by_name(skill_name)
    num_attacks = skill.trigger_okay(user.luck_roll())
    damages = []
    for target in foes:
        if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
            for _ in range(num_attacks):  # Plus pythonic que while
                damage = (user.attack * skill.power / 10) * random.uniform(0.8, 1.2)
                damage = crit_chance(user, damage)
                damages.append(damage) #pour Recoil()
                print(f"{user.name} uses {skill_name} on {target.name}! {target.name} takes {damage} damage !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage(damage)
                combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
                if target.is_defeated():
                    target.defeat()
    return damages

def one_hit_ko(user, damage):
    death = crit_chance(user, damage, 0.01)
    if death != damage :
        return True
    else:
        return False

def heal(user, team):
    target = random.choice(team.alive_members())
    heal = get_by_name("Heal")
    num_attacks = heal.trigger_okay(user.luck_roll())
    heals = []
    if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
        for _ in range(num_attacks):  # Plus pythonic que while
            damage = (user.attack * heal.power / 10) * random.uniform(0.8, 1.2)
            heals.append(damage)
            print(f"{user.name} uses Heal on {target.name}! {target.name} recovers {damage} HP !")
            num_attacks -= 1
            combat_pause(type_pause="action", attacker_name=user.name)
            target.take_damage_no_defense(damage)
            combat_pause(type_pause="heal", damage=damage, defender_name=target.name)
            target = random.choice(team.alive_members())

def recoil(list_damage, coeff, victim):
    for damage in list_damage :
        recoil = damage * coeff
        victim.take_damage_no_defense(recoil)
        if not victim.is_alive() :
            victim.health = 1
            combat_pause(type_pause="mort subite")
            

def slash(user, foes):
    generic_SU(user, foes, "slash")

def slam(user, foes):
    generic_SU(user, foes, "slam")

def smash(user, foes):
    user.take_damage(
        recoil(
            generic_SU(user, foes), 
            0.35, user)
        )
    
def shot(user, foes):
    generic_SU(user, foes, "Shot")

def panacea(user, team):
    panacea = get_by_name("Panacea")
    num_attacks = panacea.trigger_okay(user.luck_roll())
    heals = []
    for target in team.alive_members():
        if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
            for _ in range(num_attacks):  # Plus pythonic que while
                damage = (user.attack * panacea.power / 10) * random.uniform(0.8, 1.2)
                heals.append(damage)
                print(f"{user.name} uses Panacea on {target.name}! {target.name} recovers {damage} HP!")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage_no_defense(damage)
                combat_pause(type_pause="heal", damage=damage, defender_name=target.name)
    
def fire(user, foes):
    generic_SU(user, foes, "Fire")

def ice(user, foes):
    generic_SU(user, foes, "Ice")

def thunder(user, foes):
    generic_AOE(user, foes, "Thunder")

def earthquake(user, foes):
    generic_AOE(user, foes, "Earthquake")

def wind(user, foes):
    target = random.choice(foes.alive_members())
    wind = get_by_name("Wind")
    num_attacks = wind.trigger_okay(user.luck_roll())
    damages = []
    if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
        for _ in range(num_attacks):  # Plus pythonic que while
            damage = (user.attack * wind.power / 10) * random.uniform(0.8, 1.2)
            if damage >= user.attack :
                damage *= 3 #critique garanti
            else:
                damage = crit_chance(user, damage)
            damages.append(damage) #pour Recoil()
            print(f"{user.name} uses Wind on {target.name}! {target.name} takes {damage} damage !")
            num_attacks -= 1
            combat_pause(type_pause="action", attacker_name=user.name)
            target.take_damage(damage)
            combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
            if target.is_defeated():
                target.defeat()
            target = random.choice(foes.alive_members())
    return damages

def water(user, team, foes):
    all_targets = foes.alive_members() + team.alive_members()
    target = random.choice(all_targets)
    water = get_by_name("Water")
    num_attacks = water.trigger_okay(user.luck_roll())
    damages = []
    if num_attacks > 0: 
        for _ in range(num_attacks):  # Plus pythonic que while
            if user and target in team:
                heals = [] 
                damage = (user.attack * water.power / 10) * random.uniform(0.8, 1.2)
                heals.append(damage)
                print(f"{user.name} uses Water on {target.name}! {target.name} recovers {damage} HP !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage_no_defense(damage)
                combat_pause(type_pause="heal", damage=damage, defender_name=target.name)
                target = random.choice(team.alive_members())
            else:
                damage = (user.attack * water.power / 10) * random.uniform(0.8, 1.2)
                if damage >= user.attack :
                    damage *= 3 #critique garanti
                else:
                    damage = crit_chance(user, damage, 0.1)
                damages.append(damage) #pour Recoil()
                print(f"{user.name} uses Water on {target.name}! {target.name} takes {damage} damage !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage(damage)
                combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
                if target.is_defeated():
                    target.defeat()
            target = random.choice(all_targets)

def light(user, foes):
    target = foes.alive_members()
    target = random.choice(target)
    light = get_by_name("Light")
    num_attacks = light.trigger_okay(user.luck_roll())
    damages = []
    damage = (user.attack * light.power / 10) * random.uniform(0.8, 1.2)
    if one_hit_ko(user):
        target.is_alive = False
        print("ONE HIT KO !!!")
        target.defeat()
        combat_pause(type_pause="one hit ko")
    damages.append(damage) #pour Recoil()
    print(f"{user.name} uses Light on {target.name}! {target.name} takes {damage} damage !")
    num_attacks -= 1
    combat_pause(type_pause="action", attacker_name=user.name)
    target.take_damage(damage)
    combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
    if target.is_defeated():
        target.defeat()
    
    

def darkness(user, foes):
    darkness = get_by_name("Darkness")
    num_attacks = darkness.trigger_okay(user.luck_roll())
    damages = []
    for target in foes:
        if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
            for _ in range(num_attacks):  # Plus pythonic que while
                damage = (user.attack * darkness.power / 10) * random.uniform(0.8, 1.2)
                if one_hit_ko(user):
                    target.is_alive = False
                    print("ONE HIT KO !!!")
                    combat_pause(type_pause="one hit ko")
                    target.defeat()
                damages.append(damage) #pour Recoil()
                print(f"{user.name} uses Darkness on {target.name}! {target.name} takes {damage} damage !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage(damage)
                combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
                if target.is_defeated():
                    target.defeat()
    return damages
    

def void(user, foes):
    skill = get_by_name("Void")
    num_attacks = skill.trigger_okay(user.luck_roll())
    damages = []
    for target in foes:
        if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
            for _ in range(num_attacks):  # Plus pythonic que while
                damage = (user.attack * skill.power / 10) * random.uniform(0.8, 1.2)
                damage = crit_chance(user, damage)
                damages.append(damage) #pour Recoil()
                print(f"{user.name} uses Void on {target.name}! {target.name} takes {damage} damage !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage(damage)
                combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
                if target.is_defeated():
                    target.defeat()
                if not target.is_defeated():
                    target.try_lower("defense", 0.33, 0.33)
    return damages
    

def hellfire(user, foes):
    skill = get_by_name("Hellfire")
    num_attacks = skill.trigger_okay(user.luck_roll()) * 11
    damages = []
    for target in foes:
        if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
            for _ in range(num_attacks):  # Plus pythonic que while
                damage = (user.attack * skill.power / 10) * random.uniform(0.8, 1.2)
                damage = crit_chance(user, damage)
                damages.append(damage) #pour Recoil()
                print(f"{user.name} uses Hellfire on {target.name}! {target.name} takes {damage} damage !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage(damage)
                combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
                if target.is_defeated():
                    target.defeat()
    return damages

def sophisme(user, foes):
    generic_SU(user, foes, "Sophisme")

def appel_regie(user, foes):
    generic_AOE(user, foes, "Appel Regie")

# Fonctions vides pour les specials
def to_ashes(user, foes):
    target = foes.alive_members()
    target = random.choice(target)
    to_ashes = get_by_name("To Ashes")
    num_attacks = to_ashes.trigger_okay(user.luck_roll())
    while num_attacks > 1 :   
        if one_hit_ko(user):
            combat_pause(type_pause="special")
            print("Tsubaki : C'est fini!!")
            time.sleep(1)
            print(f"Tsubaki utilise To Ashes sur {target.name}")
            target.is_alive = False
            print("ONE HIT KO !!!")
            target.defeat()
            print("Tsubaki : Allez, on reprend.")
            time.sleep(3)
            target = random.choice(target)

def pacify(user, team, foes):
    pacify = get_by_name("Pacify")
    num_attacks = pacify.trigger_okay(user.luck_roll())
    heals = []
    combat_pause(type_pause="special")
    print("Shizune : N'abandonnez pas !!")
    time.sleep(1)
    print("Shizune uses Pacify")
    for target in team.alive_members():
        if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
            for _ in range(num_attacks):  # Plus pythonic que while
                damage = (user.attack * pacify.power / 4) * random.uniform(0.8, 1.2)
                heals.append(damage)
                print(f"Shizune uses Pacify on {target.name}! {target.name} recovers {damage} HP!")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage_no_defense(damage)
                combat_pause(type_pause="heal", damage=damage, defender_name=target.name)
    print("Shizune : On continue comme ça !")
    turn(team, foes)
                

def inferno(user, foes):
    skill = get_by_name("inferno")
    num_attacks = skill.trigger_okay(user.luck_roll()) * 3
    damages = []
    combat_pause(type_pause="special")
    print("Temari : Tout feu tout flamme !!")
    time.sleep(1)
    print("Temari uses Inferno")
    for target in foes:
        if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
            for _ in range(num_attacks):  # Plus pythonic que while
                damage = (user.attack * skill.power / 3) * random.uniform(0.8, 1.2)
                damage = crit_chance(user, damage)
                damages.append(damage) #pour Recoil()
                print(f"Temari uses Inferno on {target.name}! {target.name} takes {damage} damage !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage(damage)
                combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
                if target.is_defeated():
                    target.defeat()
    print("Temari : C'était chaud.")
    return damages

def tsunami(user, foes):
    skill = get_by_name("Tsunami")
    num_attacks = skill.trigger_okay(user.luck_roll())
    damages = []
    combat_pause(type_pause="special")
    print("Shiori : Bon, c'est plus drole.")
    time.sleep(1)
    print("Shiori uses Tsunami")
    for target in foes:
        if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
            for _ in range(num_attacks):  # Plus pythonic que while
                damage = (user.attack * skill.power / 3) * random.uniform(0.8, 1.2)
                damage = crit_chance(user, damage)
                damages.append(damage) #pour Recoil()
                print(f"Shiori uses Tsunami on {target.name}! {target.name} takes {damage} damage !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage(damage)
                combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
                if target.is_defeated():
                    target.defeat()
    print("Shiori : Qu'est-ce qu'on se fait chier.")
    return damages

def blizzard(user, team, foes):
    skill = get_by_name("Blizzard")
    num_attacks = skill.trigger_okay(user.luck_roll())
    damages = []
    combat_pause(type_pause="special")
    print("Gantei : On en reparle après hein.")
    time.sleep(1)
    print("Gantei uses Blizzard")
    for target in foes:
        if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
            for _ in range(num_attacks):  # Plus pythonic que while
                damage = (user.attack * skill.power / 3) * random.uniform(0.8, 1.2)
                damage = crit_chance(user, damage)
                damages.append(damage) #pour Recoil()
                print(f"Shiori uses Tsunami on {target.name}! {target.name} takes {damage} damage !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage(damage)
                combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
                if target.is_defeated():
                    target.defeat()
    print("Gantei : Alors? C'est fini ou pas?")
    turn(team, foes)

def meteor_geyser(user, team, foes):
    skill = get_by_name("Meteor Geyser")
    num_attacks = skill.trigger_okay(user.luck_roll())
    damages = []
    combat_pause(type_pause="special")
    print("Blanche : C'est partiiiiiiiii !!!!!")
    time.sleep(1)
    print("Blanche utilise Meteor Geyser")
    target = random.choice(foes.alive_members())
    if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
        for _ in range(num_attacks):  # Plus pythonic que while
            damage = (user.attack * skill.power / 3) * random.uniform(0.8, 1.2)
            if damage >= user.attack :
                damage *= 3 #critique garanti
            else:
                damage = crit_chance(user, damage)
            damages.append(damage) #pour Recoil()
            print(f"{user.name} uses Meteor Geyser on {target.name}! {target.name} takes {damage} damage !")
            num_attacks -= 1
            combat_pause(type_pause="action", attacker_name=user.name)
            target.take_damage(damage)
            combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
            if target.is_defeated():
                target.defeat()
            target = random.choice(foes.alive_members())
    print("Blanche : La classe~!")
    return damages
    
def moon(user, foes):
    skill = get_by_name("Moon")
    num_attacks = skill.trigger_okay(user.luck_roll())
    damages = []
    combat_pause(type_pause="special")
    print("Kamuri : Le pouvoir de la lune !")
    time.sleep(1)
    print("Kamuri uses Moon")
    target = random.choice(foes.alive_members())
    if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
        for _ in range(num_attacks):  # Plus pythonic que while
            damage = (user.attack * skill.power / 3) * random.uniform(0.8, 1.2)
            if damage >= user.attack :
                damage *= 3 #critique garanti
            else:
                damage = crit_chance(user, damage)
            damages.append(damage) #pour Recoil()
            print(f"{user.name} uses Moon on {target.name}! {target.name} takes {damage} damage !")
            num_attacks -= 1
            combat_pause(type_pause="action", attacker_name=user.name)
            target.take_damage_no_defense(damage)
            combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
            if target.is_defeated():
                target.defeat()
            target = random.choice(foes.alive_members())
    print("Kamuri : Ce n'est pas encore fini !")
    return damages

def sun(user, foes):
    skill = get_by_name("Meteor Geyser")
    num_attacks = skill.trigger_okay(user.luck_roll())
    damages = []
    combat_pause(type_pause="special")
    print("Asuna : Le pouvoir du soleil.")
    time.sleep(1)
    print("Asuna uses Sun")
    target = random.choice(foes.alive_members())
    if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
        for _ in range(num_attacks):  # Plus pythonic que while
            damage = (user.attack * skill.power / 3) * random.uniform(0.8, 1.2)
            if damage >= user.attack :
                damage *= 3 #critique garanti
            else:
                damage = crit_chance(user, damage)
            damages.append(damage) #pour Recoil()
            print(f"{user.name} uses Sun on {target.name}! {target.name} takes {damage} damage !")
            num_attacks -= 1
            combat_pause(type_pause="action", attacker_name=user.name)
            target.take_damage_no_defense(damage)
            combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
            if target.is_defeated():
                target.defeat()
            target = random.choice(foes.alive_members())
            recoil(damages, -1, user)
    print("Asuna: On continue comme ça.")
    return damages

def unforgettable_kind(user, foes):
    skill = get_by_name("Meteor Geyser")
    num_attacks = skill.trigger_okay(user.luck_roll())
    damages = []
    combat_pause(type_pause="special")
    print("Myosotis : Le remede à Alzheimer.")
    time.sleep(1)
    print("Myosotis uses Unforgettable Kind")
    target = random.choice(foes.alive_members())
    if num_attacks > 0:  # Vérification qu'il y a au moins une attaque
        for _ in range(num_attacks):  # Plus pythonic que while
            damage = (user.attack * skill.power / 3) * random.uniform(0.8, 1.2)
            if damage >= user.attack :
                damage *= 3 #critique garanti
            else:
                damage = crit_chance(user, damage)
            damages.append(damage) #pour Recoil()
            print(f"{user.name} uses Unforgettable Kind on {target.name}! {target.name} takes {damage} damage !")
            num_attacks -= 1
            combat_pause(type_pause="action", attacker_name=user.name)
            target.take_damage_no_defense(damage)
            combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
            if target.is_defeated():
                target.defeat()
            target = random.choice(foes.alive_members())
    print("Myosotis : Je suis inimittable.")
    return damages

def peppy_parade(user, team, foes):
    all_targets = foes.alive_members() + team.alive_members()
    target = random.choice(all_targets)
    peppy_parade = get_by_name("Peppy Parade")
    num_attacks = peppy_parade.trigger_okay(user.luck_roll())
    damages = []
    combat_pause(type_pause="special")
    print("Minori : Allez, ça va etre drole !")
    time.sleep(1)
    print("Minori uses Peppy Parade")
    if num_attacks > 0: 
        for _ in range(num_attacks):  # Plus pythonic que while
            if user and target in team:
                heals = [] 
                damage = (user.attack * peppy_parade.power / 3) * random.uniform(0.8, 1.2)
                heals.append(damage)
                print(f"{user.name} uses Peppy Parade on {target.name}! {target.name} recovers {damage} HP !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage(damage)
                combat_pause(type_pause="heal", damage=damage, defender_name=target.name)
                target = random.choice(team.alive_members())
            else:
                damage = (user.attack * water.power / 10) * random.uniform(0.8, 1.2)
                if damage >= user.attack :
                    damage *= 3 #critique garanti
                else:
                    damage = crit_chance(user, damage, 0.1)
                damages.append(damage) #pour Recoil()
                print(f"{user.name} uses Peppy Parade on {target.name}! {target.name} takes {damage} damage !")
                num_attacks -= 1
                combat_pause(type_pause="action", attacker_name=user.name)
                target.take_damage(damage)
                combat_pause(type_pause="damage", damage=damage, defender_name=target.name)
                if target.is_defeated():
                    target.defeat()
            target = random.choice(all_targets)

def the_sin_of_envy(user, team):
    characters, _ = get_characters()
    envy = get_by_name("The Sin of Envy")
    combat_pause(type_pause="special")
    print("Shiki : Et dire qu'on a encore besoin d'aide.")
    time.sleep(1)
    print("Shiki uses the Sin of Envy.")
    num_attacks = envy.trigger_okay(user.luck_roll())
    if num_attacks > 0: 
        for _ in range(num_attacks):  
            available = [char for char in characters if char not in team.members]
            if not available:
                print("Tous les personnages sont déjà dans l'équipe !")
                return None
        new_character = random.choice(available)
        team.add_member(new_character)
    return new_character
    
def summon(team):
    characters, _ = get_characters()
    # Liste des personnages pas encore dans l'équipe
    available = [char for char in characters if char not in team.members]
    if not available:
        print("Tous les personnages sont déjà dans l'équipe !")
        return None
    new_character = random.choice(available)
    team.add_member(new_character)
    print(f"{new_character.name} vous a rejoint !")
    return new_character





from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["Mycelium_Clash"]
characters = db["characters"]
monsters = db["monsters"]
scores = db["high_scores"]
skills = db["skills"]
specials = db["specials"]


character_data = [
    {"Name": "Myosotis", "HP": 1050, "Attack": 605, "Defense": 0.35, "Luck": 0.69, "Skills": ["Slash", "Smash", "Fire", "Thunder"], },
    {"Name": "Kamuri",   "HP": 1250, "Attack": 750, "Defense": 0.4, "Luck": 0.9, "Skills": ["Slam", "Heal", "Light", "Darkness"]},
    {"Name": "Asuna",    "HP": 910,  "Attack": 350, "Defense": 0.3, "Luck": 0.65, "Skills": ["Slash", "Panacea", "Earthquake", "Wind"]},
    {"Name": "Minori",   "HP": 2380, "Attack": 120, "Defense": 0.5, "Luck": 1.2, "Skills": ["Slam", "Smash", "Fire", "Light", "Thunder", "Heal", "Panacea"]},
    {"Name": "Blanche",  "HP": 780,  "Attack": 1830, "Defense": 0.25, "Luck": 0.3, "Skills": ["Slash", "Smash", "Darkness", "Void"]},
    {"Name": "Temari",   "HP": 550,  "Attack": 1560, "Defense": 0.2, "Luck": 0.56, "Skills": ["Slash", "Fire", "Hellfire", "Darkness"]},
    {"Name": "Gantei",   "HP": 1750, "Attack": 1050, "Defense": 0.45, "Luck": 0.4, "Skills": ["Slash", "Shot", "Ice", "Wind"]},
    {"Name": "Shiori",   "HP": 1640, "Attack": 470, "Defense": 0.4, "Luck": 1.0, "Skills": ["Shot", "Heal", "Water", "Panacea", "Hellfire"]},
    {"Name": "Shizune",  "HP": 2900, "Attack": 130, "Defense": 0.55, "Luck": 1.0, "Skills": ["Shot", "Panacea", "Heal", "Light"]}, 
    {"Name": "Shiki",    "HP": 1020, "Attack": 980, "Defense": 0.33, "Luck": 0.75, "Skills": ["Slash", "Smash", "Void", "Darkness", "Thunder"]},
    {"Name": "Tsubaki",  "HP": 2000, "Attack": 1550, "Defense": 0.35, "Luck": 0.34, "Skills": ["Slam", "Smash", "Fire", "Thunder"]}
]
monster_data = [
    {"Name": "Le grand Capital", "HP": 2105000, "Attack": 300, "Defense": 1, "Skills": [], "Race": "White"},
    {"Name": "Le Patriarcat",  "HP": 1940000, "Attack": 670, "Defense": 0.94,"Skills": [], "Race": "White"},
    {"Name": "Emmanuel Macron",  "HP": 4000, "Attack": 16, "Defense": 1.34,"Skills": [], "Race": "White"},
    {"Name": "L'Hégémonie Culturelle Etatsunienne",  "HP": 1040000, "Attack": 250, "Defense": 0.89,"Skills": [], "Race": "White"},
    {"Name": "Le Réchauffement Climatique",  "HP": 2500000, "Attack": 1500, "Defense": 0.8,"Skills": [], "Race" : "White"},
    {"Name": "anti-Wokes",  "HP": 1800, "Attack": 800, "Defense": 1.1,"Skills": [], "Race": "White"},
    {"Name": "Le grand déni des crimes de guerres Japonais",  "HP": 2200000, "Attack": 115, "Defense": 1.1,"Skills": [], "Race": "Asian"},
    {"Name": "Le nationalisme",  "HP": 1300000, "Attack": 400, "Defense": 1.2,"Skills": [], "Race": "White"},
    {"Name": "Bonapartiste",  "HP": 9000, "Attack": 160, "Defense": 1.3,"Skills": [], "Race": "White"},
    {"Name": "Les services de renseignement",  "HP": 5000, "Attack": 17000, "Defense": 0.7,"Skills": [], "Race": "White"},
    {"Name": "Les lobbys agro-industriels",  "HP": 750000, "Attack": 600, "Defense": 0.75, "Skills": [], "Race": "White"},
    {"Name": "Le lobby pharmaceutique",  "HP": 1100000, "Attack": 300, "Defense": 0.85, "Skills": [], "Race": "White"},
    {"Name": "La CRIF",  "HP": 2000000, "Attack": 1760, "Defense": 1.15, "Skills": [], "Race": "White"},
    {"Name": "Le consumérisme",  "HP": 1600000, "Attack": 1100, "Defense": 0.9, "Skills": [], "Race": "White"},
    {"Name": "Bobo parisien",  "HP": 3000, "Attack": 1050, "Defense": 1.2, "Skills": [],"Race": "White"},
    {"Name": "Tonton raciste", "HP": 4000, "Attack": 200, "Defense": 1.25, "Skills": [], "Race": "White"},
    {"Name": "Flic", "HP": 8500, "Attack": 1500, "Defense": 1.2, "Skills": [], "Race": "Random"}
    ]
skills_data = [
    {"Name": "Slash", "Power": 11, "Trigger": 1.0, "Description": "A quick slash attack."},
    {"Name": "Slam", "Power": 7, "Trigger": 1.1, "Description": "A light slam attack."},
    {"Name": "Smash", "Power": 45, "Trigger": 0.2, "Description": "A heavy smash attack."},
    {"Name": "Shot", "Power": 61, "Trigger": 0.5, "Description": "A fiery projectile that pierces the target."},
    {"Name": "Heal", "Power": -25, "Trigger": 1.0, "Description": "Restores health to the target."},
    {"Name": "Panacea", "Power": -13, "Trigger": 0.76, "Description": "A moderate heal for the user's team."},
    {"Name": "Fire", "Power": 26, "Trigger": 0.45, "Description": "A fiery attack that burns the target."},
    {"Name": "Ice", "Power": 18, "Trigger": 0.92, "Description": "A chilling attack that slows the target."},
    {"Name": "Thunder", "Power": 22, "Trigger": 0.88, "Description": "A shocking attack that stuns the target."},
    {"Name": "Earthquake", "Power": 30, "Trigger": 0.33, "Description": "A ground-shaking attack that damages all enemies."},
    {"Name": "Wind", "Power": 5, "Trigger": 1.32, "Description": "A swift attack with an high critical rate."},
    {"Name": "Water", "Power": 16, "Trigger": 0.95, "Description": "heals an ally, hurts an enemy."},
    {"Name": "Light", "Power": 28, "Trigger": 0.5, "Description": "A radiant attack with a 0HKO chance"},
    {"Name": "Darkness", "Power": 24, "Trigger": 0.21, "Description": "A shadow swamp AOE with a 0HKO chance"},
    {"Name": "Void", "Power": 28, "Trigger": 0.34, "Description": "A void attack that deals damage and reduces the target's defense."},
    {"Name": "Hellfire", "Power": 16, "Trigger": 0.2, "Description": "Shoots 11 times, each hit has a chance to crit."},
    {"Name": "Sophisme", "Power": 50, "Trigger": 1.1, "Description": "A basically non-argument doing mental damage"},
    {"Name": "Appel Regie", "Power": 35, "Trigger": 1.3, "Description": "Calls for help from the Regie, dealing damage to all enemies."},
    ]
specials_data = [
    {"Name": "To Ashes", "Power": 100, "Trigger": 0.1, "User": "Tsubaki", "Description": "OHKO attack that reduces the target to ashes."},
    {"Name": "Pacify", "Power": -100, "Trigger": 0.15, "User": "Shizune", "Description": "A strong heal that restores a large amount of health, grants a new turn."},
    {"Name": "Inferno", "Power": 55, "Trigger": 0.12, "User": "Temari", "Description": "Hits 3 times all enemies."},
    {"Name": "Tsunami", "Power": 101, "Trigger": 0.05, "User": "Shiori", "Description": "A massive wave that crashes down on all enemies."},
    {"Name": "Blizzard", "Power": 180, "Trigger": 0.09, "User": "Gantei", "Description": "A freezing storm that damages all enemies. grants a new turn"},
    {"Name": "Meteor Geyser", "Power": 124, "Trigger": 0.1, "User": "Blanche", "Description": "An allmighty uppercut into the sky followed by a devastating meteor strike. High crit rate."},
    {"Name": "Moon", "Power": 120, "Trigger": 0.08, "User": "Kamuri", "Description": "A mystical attack that ignores the opponent's defense."},
    {"Name": "Sun", "Power": 130, "Trigger": 0.07, "User": "Asuna", "Description": "A radiant attack that heals the user the damage dealt."},
    {"Name": "Unforgettable Kind", "Power": 140, "Trigger": 0.05, "User": "Myosotis", "Description": "A super powerful attack that reduces all damage taken to 1."},
    {"Name": "Peppy Parade", "Power": 150, "Trigger": 0.04, "User": "Minori", "Description": "Either deals massive damage or heals all allies completely."},
    {"Name": "The Sin of Envy", "Power": 200, "Trigger": 0.03, "User": "Shiki", "Description": "Summons an ally."}
    ]

def load_data():
    if characters.find_one() is None:
        characters.insert_many(character_data)
    if monsters.find_one() is None:
        monsters.insert_many(monster_data)
    if skills.find_one() is None:
        skills.insert_many(skills_data)
    if specials.find_one() is None:
        specials.insert_many(specials_data)
    skills.insert_many(specials)
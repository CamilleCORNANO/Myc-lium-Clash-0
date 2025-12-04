
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["Mycelium_Clash"]
characters = db["characters"]
monsters = db["monsters"]
scores = db["high_scores"]
skills = db["skills"]


character_data = [
    {"Name": "Myosotis", "HP": 1050, "Attack": 605, "Defense": 0.35},
    {"Name": "Kamuri",   "HP": 1250, "Attack": 750, "Defense": 0.4},
    {"Name": "Asuna",    "HP": 910,  "Attack": 350, "Defense": 0.3},
    {"Name": "Minori",   "HP": 2380, "Attack": 120, "Defense": 0.5},
    {"Name": "Blanche",  "HP": 780,  "Attack": 1830, "Defense": 0.25},
    {"Name": "Temari",   "HP": 550,  "Attack": 1560, "Defense": 0.2},
    {"Name": "Gantei",   "HP": 1750, "Attack": 1050, "Defense": 0.45},
    {"Name": "Shiori",   "HP": 1640, "Attack": 470, "Defense": 0.4},
    {"Name": "Shizune",  "HP": 2900, "Attack": 130, "Defense": 0.55},
    {"Name": "Shiki",    "HP": 1020, "Attack": 980, "Defense": 0.33},
    {"Name": "Tsubaki",  "HP": 1000, "Attack": 1000, "Defense": 0.35}
]
monster_data = [
    {"Name": "Le grand Capital", "HP": 2105000, "Attack": 300, "Defense": 1, "Race": "White"},
    {"Name": "Le Patriarcat",  "HP": 1940000, "Attack": 670, "Defense": 0.94, "Race": "White"},
    {"Name": "Emmanuel Macron",  "HP": 4000, "Attack": 16, "Defense": 1.34, "Race": "White"},
    {"Name": "L'Hégémonie Culturelle Etatsunienne",  "HP": 1040000, "Attack": 250, "Defense": 0.89, "Race": "White"},
    {"Name": "Le Réchauffement Climatique",  "HP": 2500000, "Attack": 1500, "Defense": 0.8, "Race" : "White"},
    {"Name": "anti-Wokes",  "HP": 1800, "Attack": 800, "Defense": 1.1, "Race": "White"},
    {"Name": "Le grand déni des crimes de guerres Japonais",  "HP": 2200000, "Attack": 115, "Defense": 1.1, "Race": "Asian"},
    {"Name": "Le nationalisme",  "HP": 1300000, "Attack": 400, "Defense": 1.2, "Race": "White"},
    {"Name": "Les bonapartistes",  "HP": 90000, "Attack": 160, "Defense": 1.3, "Race": "White"},
    {"Name": "Les services de renseignement",  "HP": 5000, "Attack": 17000, "Defense": 0.7, "Race": "White"},
    {"Name": "Les lobbys agro-industriels",  "HP": 750000, "Attack": 600, "Defense": 0.75, "Race": "White"},
    {"Name": "Le lobby pharmaceutique",  "HP": 1100000, "Attack": 300, "Defense": 0.85, "Race": "White"},
    {"Name": "La CRIF",  "HP": 2000000, "Attack": 1760, "Defense": 1.15, "Race": "White"},
    {"Name": "Le consumérisme",  "HP": 1600000, "Attack": 1100, "Defense": 0.9, "Race": "White"}
]
def load_data():
    if characters.find_one() is None:
        characters.insert_many(character_data)
    if monsters.find_one() is None:
        monsters.insert_many(monster_data)
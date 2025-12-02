
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["Mycelium_Clash"]
characters = db["characters"]
monsters = db["monsters"]


character_data = [
    {"Name": "Myosotis", "HP": 1050, "Attack": 605},
    {"Name": "Kamuri",   "HP": 1250, "Attack": 750},
    {"Name": "Asuna",    "HP": 910,  "Attack": 350},
    {"Name": "Minori",   "HP": 2380, "Attack": 120},
    {"Name": "Blanche",  "HP": 780,  "Attack": 1830},
    {"Name": "Temari",   "HP": 550,  "Attack": 1560},
    {"Name": "Gantei",   "HP": 1750, "Attack": 1050},
    {"Name": "Shiori",   "HP": 1640, "Attack": 470},
    {"Name": "Shizune",  "HP": 2900, "Attack": 130},
    {"Name": "Shiki",    "HP": 1020, "Attack": 980},
    {"Name": "Tsubaki",  "HP": 1000, "Attack": 1000}
]
monster_data = [
    {"Name": "Le grand Capital", "HP": 2105000, "Attack": 300},
    {"Name": "Le Patriarcat",  "HP": 1940000, "Attack": 670},
    {"Name": "Emmanuel Macron",  "HP": 4000, "Attack": 16},
    {"Name": "L'Hégémonie Culturelle Etatsunienne",  "HP": 1040000, "Attack": 250},
    {"Name": "Le Réchauffement Climatique",  "HP": 2500000, "Attack": 1500},
    {"Name": "anti-Wokes",  "HP": 1800, "Attack": 800},
    {"Name": "Le grand déni des crimes de guerres Japonais",  "HP": 2200000, "Attack": 115},
    {"Name": "Le nationalisme",  "HP": 1300000, "Attack": 400},
    {"Name": "Les bonapartistes",  "HP": 90000, "Attack": 160},
    {"Name": "Les services de renseignement",  "HP": 5000, "Attack": 17000},
    {"Name": "Les lobbys agro-industriels",  "HP": 750000, "Attack": 600},
    {"Name": "Le lobby pharmaceutique",  "HP": 1100000, "Attack": 300},
    {"Name": "La CRIF",  "HP": 2000000, "Attack": 1760},
    {"Name": "Le consumérisme",  "HP": 1600000, "Attack": 1100}
]

characters.insert_many(character_data)
monsters.insert_many(monster_data)
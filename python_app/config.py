from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "clean_hearts.db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
ROUTING_THRESHOLD = 0.25
GENERAL_SERVICES = "General Services"

OFFICER_SALT = "cleanhearts-officer-v1"
OFFICER_PASSWORD_HASH = "ecf2b5c8aa4dedd58e267b6208852c8d11abf0d7eddefea9733fd7b8441db1b4"
PBKDF2_ITERATIONS = 200_000

STATUS_LABELS = {
    "new": "New",
    "in_progress": "In progress",
    "resolved": "Resolved",
}

URGENT_KEYWORDS = [
    "flood",
    "burst",
    "gas leak",
    "fire",
    "smoke",
    "spark",
    "exposed wire",
    "electrocut",
    "injur",
    "collaps",
    "sinkhole",
    "emergency",
    "hazard",
    "accident",
    "danger",
]

DEPARTMENTS = {
    "Public Works": {
        "summary": "Roads, potholes, sidewalks, bridges, manholes and traffic signs",
        "photo": "https://images.pexels.com/photos/6018646/pexels-photo-6018646.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    },
    "Water & Drainage": {
        "summary": "Water leaks, burst pipes, sewers, drains and street flooding",
        "photo": "https://images.pexels.com/photos/28447789/pexels-photo-28447789.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    },
    "Sanitation": {
        "summary": "Rubbish, garbage bins, litter, dumping and bad smells",
        "photo": "https://images.pexels.com/photos/4651148/pexels-photo-4651148.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    },
    "Electrical & Lighting": {
        "summary": "Streetlights, power lines, electrical outages and dark streets",
        "photo": "https://images.pexels.com/photos/9971141/pexels-photo-9971141.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    },
    "Parks & Recreation": {
        "summary": "Playgrounds, swings, benches, trees, grass and green spaces",
        "photo": "https://images.pexels.com/photos/32801503/pexels-photo-32801503.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    },
    "Public Safety": {
        "summary": "Crosswalks, pedestrian signals, speeding, crime and unsafe areas",
        "photo": "https://images.pexels.com/photos/10121600/pexels-photo-10121600.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    },
    GENERAL_SERVICES: {
        "summary": "Anything else that needs a city team",
        "photo": "https://images.pexels.com/photos/11733144/pexels-photo-11733144.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
    },
}

SEED_ISSUES = [
    {
        "title": "Deep pothole on Maple Avenue near the elementary school",
        "description": "A pothole about the size of a car tire has opened in the right lane. Cars are swerving into the bike lane to avoid it, and it gets worse after every rain.",
        "address": "214 Maple Avenue, Riverside",
        "department": "Public Works",
        "priority": "normal",
        "status": "in_progress",
        "hours_ago": 48,
    },
    {
        "title": "Water main burst flooding the sidewalk",
        "description": "Water is bubbling up through the pavement and has flooded the sidewalk. Pedestrians are stepping into the road to get around it. Please send a crew as soon as possible.",
        "address": "Harbor Road, outside Baker Market",
        "department": "Water & Drainage",
        "priority": "urgent",
        "status": "new",
        "hours_ago": 1,
    },
    {
        "title": "Streetlight out for three nights on Oak Lane",
        "description": "The streetlight outside number 12 has been dark since Monday. The corner is pitch black at night and feels unsafe for people walking home.",
        "address": "Oak Lane and 5th Street",
        "department": "Electrical & Lighting",
        "priority": "normal",
        "status": "new",
        "hours_ago": 5,
    },
    {
        "title": "Overflowing bins behind the market",
        "description": "Three bins have been overflowing for a week. Rubbish is spilling onto the lane and attracting rats. The area smells terrible in the afternoon heat.",
        "address": "18 Market Lane, Eastside",
        "department": "Sanitation",
        "priority": "normal",
        "status": "resolved",
        "hours_ago": 96,
    },
    {
        "title": "Broken swing and rusted slide at Willow Park",
        "description": "One of the swings has snapped its chain and the slide has rusted through near the bottom. Several families have stopped bringing their children here.",
        "address": "Willow Park, north playground",
        "department": "Parks & Recreation",
        "priority": "normal",
        "status": "new",
        "hours_ago": 24,
    },
    {
        "title": "Crosswalk signal never gives pedestrians a walk sign",
        "description": "Pedestrians wait several minutes and the walk signal never appears. Children crossing to school are taking a real risk. This is a safety hazard.",
        "address": "Pine Street and Central Avenue",
        "department": "Public Safety",
        "priority": "urgent",
        "status": "in_progress",
        "hours_ago": 3,
    },
]

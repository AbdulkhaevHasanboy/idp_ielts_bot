"""
Location and GPS Venue Resolver for IDP IELTS Test Centres across Uzbekistan.
"""
import re
import urllib.parse
import requests
from data.test_centers import TEST_CENTERS

CITY_ALIASES = {
    "andijan": ["andijon", "anidjon", "andijan", "andijonda", "andijondagi", "andijondegi"],
    "tashkent_ciu": ["toshkent", "tashkent", "toshken", "ciu", "novza", "bunyodkor", "toshkentda", "toshkentdagi", "toshkentdegi"],
    "tashkent_afrosiyob": ["oybek", "afrosiyob", "bosh ofis", "edu-action ofis", "eduaction ofis"],
    "samarkand": ["samarqand", "samarkand", "samarqanda", "samarqanddagi", "samarqanddegi", "dagbitskaya"],
    "fergana": ["farg'ona", "fargona", "fergana", "fergana", "farg'onada", "farg'onadagi"],
    "namangan": ["namangan", "namanganda", "namangandagi", "namangandegi"],
    "bukhara": ["buxoro", "bukhara", "buxoroda", "buxorodagi", "buxorodegi", "naqshband"],
    "urgench": ["urganch", "urgench", "xorazm", "khorezm", "urganchda", "urganchdagi"],
    "nukus": ["nukus", "qoraqalpog'iston", "karakalpakstan", "nukusda", "nukusdagi"],
    "navoi": ["navoiy", "navoi", "navoy", "navoiyda", "navoiydagi"],
    "termez": ["termiz", "termez", "surxondaryo", "termizda", "termizdagi"]
}

LOCATION_KEYWORDS = [
    "map", "xarita", "karta", "lokatsiya", "qayerda", "joylashuvi",
    "joylashgan", "manzil", "adres", "korsat", "ko'rsat", "yubor",
    "where", "location", "venue", "gps"
]

def detect_city_in_text(text: str) -> str | None:
    """Finds which IDP IELTS test center city is mentioned in the text."""
    lower = text.lower()
    for center_id, aliases in CITY_ALIASES.items():
        for alias in aliases:
            # Match whole word or substring
            if alias in lower:
                return center_id
    return None

def is_location_request(text: str) -> bool:
    """Checks if the user is asking for a location, map, or venue."""
    lower = text.lower()
    return any(k in lower for k in LOCATION_KEYWORDS)

def geocode_place(query: str) -> dict | None:
    """Fallback geocoder using OpenStreetMap Nominatim for any custom place."""
    clean_query = query.strip()
    if not clean_query.lower().endswith("uzbekistan") and not clean_query.lower().endswith("o'zbekiston"):
        clean_query += ", Uzbekistan"
    
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(clean_query)}&format=json&limit=1"
    headers = {"User-Agent": "IDPIELTSUzbekistanBot/1.0"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200 and r.json():
            data = r.json()[0]
            return {
                "latitude": float(data["lat"]),
                "longitude": float(data["lon"]),
                "title": data["display_name"].split(",")[0],
                "address": data["display_name"]
            }
    except Exception:
        pass
    return None

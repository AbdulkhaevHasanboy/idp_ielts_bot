import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

# Official IDP IELTS Uzbekistan Links & Info
IDP_UZBEKISTAN_URL = "https://ielts.idp.com/uzbekistan"
EDU_ACTION_URL = "https://edu-action.uz"
IDP_BOOKING_URL = "https://ielts.idp.com/uzbekistan/test-dates"
IDP_RESULTS_URL = "https://ielts.idp.com/results/check-your-result"
IDP_OSR_URL = "https://ielts.idp.com/about/one-skill-retake"

SUPPORT_PHONE = "+998 71 148 86 86"
SUPPORT_TELEGRAM = "https://t.me/idp555"
SUPPORT_USERNAME = "@idp555"
SUPPORT_INSTAGRAM = "https://instagram.com/idp_ielts_uzbekistan"

CURRENT_IELTS_PRICE = "2,664,000 UZS"
CURRENT_UKVI_PRICE = "2,980,000 UZS"
CURRENT_LIFE_SKILLS_PRICE = "2,627,000 UZS"
CURRENT_OSR_PRICE = "1,850,000 UZS"

DATABASE_PATH = os.getenv("DATABASE_PATH", "/home/xasanboy/idp_ielts_bot/data/bot_database.db")

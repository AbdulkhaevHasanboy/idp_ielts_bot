import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7496849798:AAGv1q5BZslsaP_EMJstgYZoCMAXqpyj6f8")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBacolReTbdf-JPXv-XhTzPRigBabXGgCw")
GEMINI_MODEL = "gemini-2.5-flash"

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

CURRENT_IELTS_PRICE = "2,665,000 UZS"
CURRENT_UKVI_PRICE = "2,850,000 UZS"
CURRENT_OSR_PRICE = "1,850,000 UZS"

DATABASE_PATH = "/home/xasanboy/idp_ielts_bot/data/bot_database.db"

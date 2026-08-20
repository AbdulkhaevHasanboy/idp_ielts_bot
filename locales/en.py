"""
English language localization strings and templates for IDP IELTS Bot.
"""

STRINGS = {
    "welcome": """Hello, {name}! 🇬🇧

Welcome to the official *IDP IELTS Uzbekistan* AI Assistant Bot!

I am your personal AI IELTS Tutor & Guide:
✨ *AI Intelligence:* Ask me any question, send a photo of your handwritten essay (Writing) or a voice note (Speaking) — I will provide instant, in-depth evaluation and Band 9 feedback!
🎯 *Daily Quiz Challenge:* Practice authentic exam questions and learn key traps.
🗣 *Speaking Simulator:* Access Part 2 cue cards and model answers.
📚 *Band 9 Flashcards:* Master high-level academic vocabulary and idioms.
📍 *Test Centres & GPS:* Find official IDP venues in Uzbekistan with direct map pins.
📊 *Band Calculator:* Convert your raw scores to official IELTS Band scores.

Select an option from the menu below or simply send your question! 👇""",

    "main_menu_title": "🏠 *Main Menu:*",

    "btn_centers": "📍 Centres & Locations",
    "btn_quiz": "🎯 Daily Quiz Challenge",
    "btn_speaking_sim": "🗣 Speaking Simulator",
    "btn_flashcards": "📚 Band 9 Flashcards",
    "btn_calculator": "📊 Band Calculator",
    "btn_register": "📝 Registration & Fees",
    "btn_retake": "🔄 One Skill Retake (OSR)",
    "btn_contact": "📞 Contact & Support",
    "btn_lang": "🌐 Change Language",

    "regions_title": """📍 *Official IDP IELTS Test Centres in Uzbekistan:*

Select your region to view centres and *request GPS location pins*: 👇""",

    "center_detail_template": """🏛 *{title}*

📍 *Address:* {address}
📞 *Phone:* `{phone}`
⏰ *Working Hours:* {work_hours}
📝 *Available Test Types:* {types}

Tap the button below to get the direct venue location pin in Telegram: 👇""",

    "btn_send_venue": "📍 Show on Map (Location Pin)",
    "btn_back_centers": "◀️ Back to Regions",
    "btn_back_main": "🏠 Main Menu",

    "calc_menu_title": """📊 *IELTS Band Calculator:*

Select a component or test format to calculate your score:""",

    "btn_calc_listening": "🎧 Listening (0-40)",
    "btn_calc_reading_acad": "📖 Reading Academic (0-40)",
    "btn_calc_reading_gen": "📰 Reading General (0-40)",
    "btn_calc_overall": "🎯 Overall Band Score",

    "calc_listening_prompt": "🎧 *Listening Band Calculator:*\n\nEnter your raw score from 1 to 40 (e.g. `34`):",
    "calc_reading_acad_prompt": "📖 *Reading Academic Band Calculator:*\n\nEnter your raw score from 1 to 40 (e.g. `32`):",
    "calc_reading_gen_prompt": "📰 *Reading General Band Calculator:*\n\nEnter your raw score from 1 to 40 (e.g. `35`):",
    "calc_overall_prompt": "🎯 *Overall Band Calculator:*\n\nEnter your 4 module scores separated by a space:\n`Listening Reading Writing Speaking`\n\nExample: `7.5 7.0 6.5 7.0`",

    "register_info": """📝 *IDP IELTS Registration & Pricing:*

💰 *Official Test Fees (Uzbekistan):*
• *IELTS Academic / General (Computer):* 2,664,000 UZS (~$205)
• *IELTS for UKVI (Academic/General):* 2,980,000 UZS
• *IELTS Life Skills (A1/B1):* 2,627,000 UZS
• *One Skill Retake (OSR):* 1,850,000 UZS

🏛 *State Compensation (my.gov.uz):*
In Uzbekistan, candidates who score *Band 7.0 (C1)* or higher on the official exam can apply via the [my.gov.uz](https://my.gov.uz) portal for 100% government reimbursement of their exam fee!

📌 *Registration Steps:*
1. Visit [ielts.idp.com/uzbekistan](https://ielts.idp.com/uzbekistan).
2. Choose your preferred city, date, and format.
3. Enter your details exactly as written in your International Passport and upload passport scan.
4. Complete payment via Uzcard, Humo, Visa, or Mastercard.

⚠️ *Important:* You MUST bring your ORIGINAL valid passport/ID card on test day!""",

    "contact_info": """📞 *IDP IELTS Uzbekistan Contact Centre:*

👤 *Telegram Support Team Member:*
[@idp555](https://t.me/idp555)

☎️ *Single Call Centre:*
`+998 71 148 86 86`

🏢 *Head Office (Edu-Action):*
16 Afrosiyob Street, Mirobod district, Tashkent (Oybek metro)

🌐 *Official Websites:*
• [ielts.idp.com/uzbekistan](https://ielts.idp.com/uzbekistan)
• [edu-action.uz](https://edu-action.uz)

📱 *Instagram:* [@idp_ielts_uzbekistan](https://instagram.com/idp_ielts_uzbekistan)""",

    "lang_changed": "✅ Language successfully switched to *English* 🇬🇧",
    "choose_lang": "🌐 Please select your language / Iltimos, tilni tanlang / Please select language:",
    "invalid_number": "⚠️ Please enter an integer between 0 and 40!",
    "invalid_overall": "⚠️ Please enter 4 numbers separated by spaces (e.g. `7.0 6.5 6.0 7.0`), range 0 to 9.",
    "ai_analyzing_image": "🔍 *Analyzing image...* (Evaluating against official IELTS criteria, please wait)",
    "ai_analyzing_audio": "🎙 *Analyzing audio recording...* (Evaluating Speaking criteria, please wait)"
}

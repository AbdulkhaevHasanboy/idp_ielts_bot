"""
Uzbek language localization strings and templates for IDP IELTS Bot.
"""

STRINGS = {
    "welcome": """Assalomu alaykum, {name}! 🇺🇿

*IDP IELTS Uzbekistan* AI yordamchi botiga xush kelibsiz!

Men IDP IELTS bo'yicha sizning shaxsiy aqlli murabbiyingizman:
✨ *Sun'iy intellekt (AI):* Menga istalgan savolingizni yozing, insho (essay) rasmini, test topshiriqlarini yoki ovozli xabar (Speaking) yuboring — bir zumda to'liq tahlil va maslahat beraman!
🎯 *Kunlik Quiz & Mashqlar:* Imtihon savollarini yechib bilimlaringizni sinab boring.
🗣 *Speaking Trenajyor:* Part 2 mavzulari va Band 9 model javoblar bilan mashq qiling.
📚 *Band 9 So'z Boyligi:* Har kuni yuqori ball beruvchi akademik iboralarni o'rganing.
📍 *Markazlar & GPS Xarita:* O'zbekistondagi barcha IDP markazlariga to'g'ridan-to'g'ri xarita oling.
📊 *Band Kalkulyator:* To'g'ri javoblaringiz sonidan aniq IELTS balingizni hisoblang.

Quyidagi menyudan kerakli bo'limni tanlang yoki shunchaki yozing! 👇""",

    "main_menu_title": "🏠 *Asosiy Menyu:*",

    "btn_centers": "📍 Markazlar & Lokatsiyalar",
    "btn_quiz": "🎯 Kunlik Quiz (Challenge)",
    "btn_speaking_sim": "🗣 Speaking Trenajyor",
    "btn_flashcards": "📚 Band 9 So'zlar (Cards)",
    "btn_calculator": "📊 Band Kalkulyator",
    "btn_register": "📝 Ro'yxatdan o'tish & Narxlar",
    "btn_retake": "🔄 One Skill Retake (OSR)",
    "btn_contact": "📞 Bog'lanish & Aloqa",
    "btn_lang": "🌐 Tilni o'zgartirish",

    "regions_title": """📍 *O'zbekistondagi IDP IELTS markazlari:*

Hududingizni tanlang va markaz haqida to'liq ma'lumot hamda *GPS lokatsiyani* oling: 👇""",

    "center_detail_template": """🏛 *{title}*

📍 *Manzil:* {address}
📞 *Telefon:* `{phone}`
⏰ *Ish vaqti:* {work_hours}
📝 *Imtihon turlari:* {types}

Pastdagi tugma orqali markazning aniq lokatsiyasini Telegram xaritada olishingiz mumkin: 👇""",

    "btn_send_venue": "📍 Xaritada ko'rsatish (Lokatsiya)",
    "btn_back_centers": "◀️ Hududlarga qaytish",
    "btn_back_main": "🏠 Asosiy menyu",

    "calc_menu_title": """📊 *IELTS Band Kalkulyatori:*

Qaysi modul yoki test turining balini hisoblamoqchisiz?""",

    "btn_calc_listening": "🎧 Listening (0-40)",
    "btn_calc_reading_acad": "📖 Reading Academic (0-40)",
    "btn_calc_reading_gen": "📰 Reading General (0-40)",
    "btn_calc_overall": "🎯 Overall (Umumiy) Band",

    "calc_listening_prompt": "🎧 *Listening Band Hisoblagich:*\n\n1 tadan 40 tagacha to'g'ri javoblaringiz sonini kiriting (masalan: `34` yoki `28`):",
    "calc_reading_acad_prompt": "📖 *Reading Academic Band Hisoblagich:*\n\n1 tadan 40 tagacha to'g'ri javoblaringiz sonini kiriting (masalan: `32`):",
    "calc_reading_gen_prompt": "📰 *Reading General Band Hisoblagich:*\n\n1 tadan 40 tagacha to'g'ri javoblaringiz sonini kiriting (masalan: `35`):",
    "calc_overall_prompt": "🎯 *Overall Band Hisoblagich:*\n\n4 ta modul ballaringizni quyidagi formatda kiriting:\n`Listening Reading Writing Speaking`\n\nMisol uchun: `7.5 7.0 6.5 7.0`",

    "register_info": """📝 *IDP IELTS Imtihoniga Ro'yxatdan O'tish va Narxlar:*

💰 *Joriy rasmiy narxlar (O'zbekiston):*
• *IELTS Academic / General (Computer):* 2,664,000 UZS
• *IELTS for UKVI (Academic/General):* 2,980,000 UZS
• *IELTS Life Skills (A1/B1):* 2,627,000 UZS
• *One Skill Retake (OSR):* 1,850,000 UZS

🏛 *Davlat Kompensatsiyasi (my.gov.uz):*
O'zbekistonda rasmiy imtihonda *7.0 (C1)* yoki undan yuqori ball to'plagan yoshlar [my.gov.uz](https://my.gov.uz) portali orqali imtihon xarajatini davlatdan 100% to'liq qaytarib olishlari (kompensatsiya) mumkin!

📌 *Ro'yxatdan o'tish bosqichlari:*
1. [ielts.idp.com/uzbekistan](https://ielts.idp.com/uzbekistan) rasmiy saytiga kiring.
2. Shahar, qulay sana va formatni tanlang.
3. Pasportingizdagi shaxsiy ma'lumotlarni to'ldiring va skanini yuklang.
4. To'lovni Uzcard, Humo, Visa yoki Mastercard orqali bajaring.

⚠️ *Eslatma:* Imtihon kuni faqat va faqat ASL (original) pasport yoki ID kartani olib kelish shart!""",

    "contact_info": """📞 *IDP IELTS Uzbekistan Aloqa Markazi:*

👤 *Telegram qo'llab-quvvatlash xodimi:*
[@idp555](https://t.me/idp555)

☎️ *Yagona aloqa markazi (Call Centre):*
`+998 71 148 86 86`

🏢 *Bosh ofis (Edu-Action):*
Afrosiyob ko'chasi 16-uy, Mirobod tumani, Toshkent (Oybek metrosi)

🌐 *Rasmiy veb-saytlar:*
• [ielts.idp.com/uzbekistan](https://ielts.idp.com/uzbekistan)
• [edu-action.uz](https://edu-action.uz)

📱 *Instagram:* [@idp_ielts_uzbekistan](https://instagram.com/idp_ielts_uzbekistan)""",

    "lang_changed": "✅ Til muvaffaqiyatli o'zgartirildi: *O'zbekcha* 🇺🇿",
    "choose_lang": "🌐 Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please select language:",
    "invalid_number": "⚠️ Iltimos, 0 dan 40 gacha bo'lgan butun son kiriting!",
    "invalid_overall": "⚠️ Iltimos, 4 ta sonni probel bilan kiriting (masalan: `7.0 6.5 6.0 7.0`), ballar 0 dan 9 gacha bo'lishi lozim.",
    "ai_analyzing_image": "🔍 *Rasm tahlil qilinmoqda...* (IELTS Writing/Reading/TRF mezonlari bo'yicha tekshirilmoqda, iltimos kuting)",
    "ai_analyzing_audio": "🎙 *Ovozli xabar tinglanmoqda...* (IELTS Speaking mezonlari bo'yicha tekshirilmoqda, iltimos kuting)"
}

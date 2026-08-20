"""
Russian language localization strings and templates for IDP IELTS Bot.
"""

STRINGS = {
    "welcome": """Здравствуйте, {name}! 🇷🇺

Добро пожаловать в официальный AI бот-помощник *IDP IELTS Uzbekistan*!

Я ваш персональный интеллектуальный наставник по IELTS:
✨ *Искусственный интеллект (AI):* Задайте любой вопрос, отправьте фото эссе (Writing) или аудиозапись ответа (Speaking) — я мгновенно оценю по критериям IELTS и дам советы!
🎯 *Ежедневный квиз:* Тренируйтесь на реальных экзаменационных вопросах.
🗣 *Speaking Тренажер:* Темы Part 2 и образцовые ответы Band 9.
📚 *Band 9 Карточки:* Изучайте академические слова и устойчивые выражения.
📍 *Тест-центры и GPS:* Получайте точные локации центров IDP в Узбекистане.
📊 *Калькулятор баллов:* Рассчитайте свой IELTS Band из количества правильных ответов.

Выберите нужный раздел или просто напишите ваш вопрос! 👇""",

    "main_menu_title": "🏠 *Главное меню:*",

    "btn_centers": "📍 Центры и Локации",
    "btn_quiz": "🎯 Ежедневный Квиз",
    "btn_speaking_sim": "🗣 Speaking Тренажер",
    "btn_flashcards": "📚 Band 9 Слова (Cards)",
    "btn_calculator": "📊 Калькулятор баллов",
    "btn_register": "📝 Регистрация и Цены",
    "btn_retake": "🔄 One Skill Retake (OSR)",
    "btn_contact": "📞 Контакты и Связь",
    "btn_lang": "🌐 Сменить язык",

    "regions_title": """📍 *Тест-центры IDP IELTS в Узбекистане:*

Выберите ваш регион, чтобы узнать подробности и *получить GPS-локацию*: 👇""",

    "center_detail_template": """🏛 *{title}*

📍 *Адрес:* {address}
📞 *Телефон:* `{phone}`
⏰ *Режим работы:* {work_hours}
📝 *Форматы экзамена:* {types}

Нажмите кнопку ниже, чтобы отправить точную локацию прямо в Telegram: 👇""",

    "btn_send_venue": "📍 Показать на карте (Локация)",
    "btn_back_centers": "◀️ Назад к регионам",
    "btn_back_main": "🏠 Главное меню",

    "calc_menu_title": """📊 *Калькулятор IELTS Band:*

Какой модуль или формат вы хотите рассчитать?""",

    "btn_calc_listening": "🎧 Listening (0-40)",
    "btn_calc_reading_acad": "📖 Reading Academic (0-40)",
    "btn_calc_reading_gen": "📰 Reading General (0-40)",
    "btn_calc_overall": "🎯 Overall (Общий) Band",

    "calc_listening_prompt": "🎧 *Калькулятор Listening:*\n\nВведите количество правильных ответов от 1 до 40 (например: `34`):",
    "calc_reading_acad_prompt": "📖 *Калькулятор Reading Academic:*\n\nВведите количество правильных ответов от 1 до 40 (например: `32`):",
    "calc_reading_gen_prompt": "📰 *Калькулятор Reading General:*\n\nВведите количество правильных ответов от 1 до 40 (например: `35`):",
    "calc_overall_prompt": "🎯 *Калькулятор Overall Band:*\n\nВведите ваши 4 балла через пробел:\n`Listening Reading Writing Speaking`\n\nПример: `7.5 7.0 6.5 7.0`",

    "register_info": """📝 *Регистрация на IDP IELTS и Стоимость:*

💰 *Официальные цены (Узбекистан):*
• *IELTS Academic / General (Computer):* 2 664 000 сум
• *IELTS for UKVI (Academic/General):* 2 980 000 сум
• *IELTS Life Skills (A1/B1):* 2 627 000 сум
• *One Skill Retake (OSR):* 1 850 000 сум

🏛 *Государственная компенсация (my.gov.uz):*
В Узбекистане кандидаты, сдавшие экзамен на балл *7.0 (C1)* и выше, могут подать заявку через портал [my.gov.uz](https://my.gov.uz) на 100% возмещение стоимости экзамена государством!

📌 *Шаги для регистрации:*
1. Перейдите на [ielts.idp.com/uzbekistan](https://ielts.idp.com/uzbekistan).
2. Выберите город, дату и формат.
3. Заполните данные и загрузите скан загранпаспорта.
4. Оплатите картой Uzcard, Humo, Visa или Mastercard.

⚠️ *Важно:* В день экзамена обязателен ОРИГИНАЛ паспорта/ID карты!""",

    "contact_info": """📞 *Контакты IDP IELTS Uzbekistan:*

👤 *Сотрудник поддержки в Telegram:*
[@idp555](https://t.me/idp555)

☎️ *Единый колл-центр:*
`+998 71 148 86 86`

🏢 *Главный офис (Edu-Action):*
ул. Афросиёб 16, Мирабадский район, Ташкент (м. Ойбек)

🌐 *Официальные сайты:*
• [ielts.idp.com/uzbekistan](https://ielts.idp.com/uzbekistan)
• [edu-action.uz](https://edu-action.uz)

📱 *Instagram:* [@idp_ielts_uzbekistan](https://instagram.com/idp_ielts_uzbekistan)""",

    "lang_changed": "✅ Язык успешно изменен на *Русский* 🇷🇺",
    "choose_lang": "🌐 Пожалуйста, выберите язык / Iltimos, tilni tanlang / Please select language:",
    "invalid_number": "⚠️ Пожалуйста, введите целое число от 0 до 40!",
    "invalid_overall": "⚠️ Введите 4 числа через пробел (например: `7.0 6.5 6.0 7.0`), диапазон от 0 до 9.",
    "ai_analyzing_image": "🔍 *Анализ изображения...* (Проверка по критериям IELTS, пожалуйста, подождите)",
    "ai_analyzing_audio": "🎙 *Анализ аудиозаписи...* (Оценка Speaking по критериям IELTS, пожалуйста, подождите)"
}

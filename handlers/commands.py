"""
Telegram command handlers for IDP IELTS Bot.
"""
from telegram import Update
from telegram.ext import ContextTypes
from services.user_state import get_user_language, set_user_language, set_user_state
from locales import t
from keyboards import (
    get_main_reply_keyboard,
    get_regions_inline_keyboard,
    get_calculator_menu_keyboard,
    get_quiz_keyboard,
    get_speaking_cue_keyboard,
    get_flashcard_keyboard,
    get_retake_keyboard,
    get_language_keyboard
)
from data.interactive_content import QUIZ_QUESTIONS, SPEAKING_CUE_CARDS, BAND9_FLASHCARDS
from data.ielts_knowledge import ONE_SKILL_RETAKE_INFO

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    set_user_language(user.id, lang, user.username, user.first_name)
    set_user_state(user.id, "NONE")

    welcome_text = t("welcome", lang, name=user.first_name or "Talabgor")
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_reply_keyboard(lang),
        parse_mode="Markdown"
    )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    
    if lang == "uz":
        help_text = """✨ *IDP IELTS AI Bot Imkoniyatlari:*

🤖 *AI Yordamchi:* Menga istalgan savolingizni yozing, insho (essay) rasmini yoki speaking ovozli xabarini yuboring — bir zumda baholab xatolaringizni to'g'irlab beraman!
🎯 /quiz - Kunlik IELTS mashqlari va test tuzoqlari
🗣 /speaking - Speaking Part 2 trenajyori va Band 9 namunalar
📚 /flashcards - Band 9 so'z boyligi kartalari
📍 /centers - O'zbekistondagi IDP test markazlari va GPS xarita
📊 /calculator - IELTS Band ball hisoblagichi
🔄 /retake - One Skill Retake (OSR) haqida
📝 /dates - Imtihon sanalari va narxlar
📞 /contact - Edu-Action / IDP Uzbekistan aloqa markazi
🌐 /lang - Tilni o'zgartirish (O'zbek / Русский / English)"""
    elif lang == "ru":
        help_text = """✨ *Возможности IDP IELTS AI Бота:*

🤖 *AI Помощник:* Отправьте мне любой вопрос, фото эссе или голосовое сообщение — я проверю и дам оценку по критериям IELTS!
🎯 /quiz - Ежедневный квиз и разбор ловушек
🗣 /speaking - Speaking Part 2 тренажер и образцы Band 9
📚 /flashcards - Карточки академических слов Band 9
📍 /centers - Центры IDP IELTS и GPS локации
📊 /calculator - Калькулятор баллов IELTS Band
🔄 /retake - Информация о One Skill Retake
📝 /dates - Даты экзаменов и регистрация
📞 /contact - Контакты IDP IELTS Uzbekistan
🌐 /lang - Сменить язык"""
    else:
        help_text = """✨ *IDP IELTS AI Bot Features:*

🤖 *AI Assistant:* Send any question, essay photo, or speaking voice note — I will grade and provide Band 9 feedback!
🎯 /quiz - Daily IELTS practice challenge & tips
🗣 /speaking - Speaking Part 2 simulator & model answers
📚 /flashcards - Band 9 vocabulary flashcards
📍 /centers - Test centres across Uzbekistan & GPS map pins
📊 /calculator - Official IELTS Band calculator
🔄 /retake - One Skill Retake (OSR) Guide
📝 /dates - Test dates & registration
📞 /contact - IDP Uzbekistan Contacts
🌐 /lang - Switch language"""

    await update.message.reply_text(
        help_text,
        reply_markup=get_main_reply_keyboard(lang),
        parse_mode="Markdown"
    )

async def cmd_centers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    await update.message.reply_text(
        t("regions_title", lang),
        reply_markup=get_regions_inline_keyboard(lang),
        parse_mode="Markdown"
    )

async def cmd_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    q_data = QUIZ_QUESTIONS[0]
    q_text = q_data.get(f"question_{lang}", q_data["question_uz"])
    opts = "\n".join(q_data["options"])
    full_text = f"{q_text}\n\n{opts}\n\n👇 *Variantlardan birini tanlang:*"
    await update.message.reply_text(
        full_text,
        reply_markup=get_quiz_keyboard(1, lang=lang),
        parse_mode="Markdown"
    )

async def cmd_speaking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    card = SPEAKING_CUE_CARDS[0]
    cues_text = "\n".join([f"• {c}" for c in card["cues"]])
    card_text = f"""🗣 *IELTS Speaking Part 2 Cue Card (#{card['id']}):*

📌 *Topic:* *{card['topic']}*

You should say:
{cues_text}

⏱ _Sizda reja tuzish uchun 1 daqiqa vaqt bor. So'ng 2 daqiqa davomida gapirishingiz kerak._"""
    await update.message.reply_text(
        card_text,
        reply_markup=get_speaking_cue_keyboard(1, show_model=False, lang=lang),
        parse_mode="Markdown"
    )

async def cmd_flashcards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    card = BAND9_FLASHCARDS[0]
    meaning = card.get(f"meaning_{lang}", card["meaning_uz"])
    f_text = f"""📚 *Band 9 Academic Vocabulary Flashcard (1/{len(BAND9_FLASHCARDS)}):*

💎 *Word:* `{card['word']}`
🗣 *Pronunciation:* `{card['phonetic']}`
📖 *Meaning:* {meaning}
🔗 *Collocation:* `{card['collocation']}`

📝 *IELTS Example Sentence:*
_{card['ielts_sentence']}_"""
    await update.message.reply_text(
        f_text,
        reply_markup=get_flashcard_keyboard(0, lang=lang),
        parse_mode="Markdown"
    )

async def cmd_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    await update.message.reply_text(
        t("calc_menu_title", lang),
        reply_markup=get_calculator_menu_keyboard(lang),
        parse_mode="Markdown"
    )

async def cmd_retake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    info_text = ONE_SKILL_RETAKE_INFO.get(lang, ONE_SKILL_RETAKE_INFO["uz"])
    await update.message.reply_text(
        info_text,
        reply_markup=get_retake_keyboard(lang),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def cmd_dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    await update.message.reply_text(
        t("register_info", lang),
        reply_markup=get_main_reply_keyboard(lang),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def cmd_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    await update.message.reply_text(
        t("contact_info", lang),
        reply_markup=get_main_reply_keyboard(lang),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def cmd_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    await update.message.reply_text(
        t("choose_lang", lang),
        reply_markup=get_language_keyboard(),
        parse_mode="Markdown"
    )

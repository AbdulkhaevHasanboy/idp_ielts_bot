"""
Message text handlers, dynamic button dispatching, calculation input processing,
and seamless AI conversational intelligence with instant native Telegram Map / Venue delivery.
"""
import re
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from services.user_state import get_user_language, get_user_state, set_user_state
from locales import t
from data.test_centers import TEST_CENTERS
from data.interactive_content import QUIZ_QUESTIONS, SPEAKING_CUE_CARDS, BAND9_FLASHCARDS
from data.ielts_knowledge import ONE_SKILL_RETAKE_INFO
from services.calculator import (
    get_listening_band,
    get_academic_reading_band,
    get_general_reading_band,
    calculate_overall_band,
    get_band_feedback
)
from services.location_service import detect_city_in_text, is_location_request, geocode_place
from services.ai_service import generate_ai_chat_response
from keyboards import (
    get_main_reply_keyboard,
    get_regions_inline_keyboard,
    get_calculator_menu_keyboard,
    get_quiz_keyboard,
    get_speaking_cue_keyboard,
    get_flashcard_keyboard,
    get_retake_keyboard,
    get_language_keyboard,
    get_center_detail_keyboard
)
from config import IDP_BOOKING_URL

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.effective_user
    lang = get_user_language(user.id)
    user_state = get_user_state(user.id)
    state = user_state.get("state", "NONE")
    calc_mode = user_state.get("calc_mode")
    last_center_id = user_state.get("last_center_id")

    # 1. Main Reply Keyboard Button Matching
    if text in [t("btn_centers", "uz"), t("btn_centers", "ru"), t("btn_centers", "en"), "📍 Markazlar & Lokatsiyalar", "📍 Центры и Локации", "📍 Centres & Locations"]:
        set_user_state(user.id, "NONE")
        await update.message.reply_text(
            t("regions_title", lang),
            reply_markup=get_regions_inline_keyboard(lang),
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown"
        )
        return

    if text in [t("btn_quiz", "uz"), t("btn_quiz", "ru"), t("btn_quiz", "en"), "🎯 Kunlik Quiz (Challenge)", "🎯 Ежедневный Квиз", "🎯 Daily Quiz Challenge"]:
        set_user_state(user.id, "NONE")
        q_data = QUIZ_QUESTIONS[0]
        q_text = q_data.get(f"question_{lang}", q_data["question_uz"])
        opts = "\n".join(q_data["options"])
        full_text = f"{q_text}\n\n{opts}\n\n👇 *Variantlardan birini tanlang:*"
        await update.message.reply_text(
            full_text,
            reply_markup=get_quiz_keyboard(1, lang=lang),
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown"
        )
        return

    if text in [t("btn_speaking_sim", "uz"), t("btn_speaking_sim", "ru"), t("btn_speaking_sim", "en"), "🗣 Speaking Trenajyor", "🗣 Speaking Тренажер", "🗣 Speaking Simulator"]:
        set_user_state(user.id, "NONE")
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
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown"
        )
        return

    if text in [t("btn_flashcards", "uz"), t("btn_flashcards", "ru"), t("btn_flashcards", "en"), "📚 Band 9 So'zlar (Cards)", "📚 Band 9 Слова (Cards)", "📚 Band 9 Flashcards"]:
        set_user_state(user.id, "NONE")
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
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown"
        )
        return

    if text in [t("btn_calculator", "uz"), t("btn_calculator", "ru"), t("btn_calculator", "en"), "📊 Band Kalkulyator", "📊 Калькулятор баллов", "📊 Band Calculator"]:
        set_user_state(user.id, "NONE")
        await update.message.reply_text(
            t("calc_menu_title", lang),
            reply_markup=get_calculator_menu_keyboard(lang),
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown"
        )
        return

    if text in [t("btn_register", "uz"), t("btn_register", "ru"), t("btn_register", "en"), "📝 Ro'yxatdan o'tish & Narxlar", "📝 Регистрация и Цены", "📝 Registration & Fees"]:
        set_user_state(user.id, "NONE")
        await update.message.reply_text(
            t("register_info", lang),
            reply_markup=get_main_reply_keyboard(lang),
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

    if text in [t("btn_retake", "uz"), t("btn_retake", "ru"), t("btn_retake", "en"), "🔄 One Skill Retake (OSR)"]:
        set_user_state(user.id, "NONE")
        info_text = ONE_SKILL_RETAKE_INFO.get(lang, ONE_SKILL_RETAKE_INFO["uz"])
        await update.message.reply_text(
            info_text,
            reply_markup=get_retake_keyboard(lang),
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

    if text in [t("btn_contact", "uz"), t("btn_contact", "ru"), t("btn_contact", "en"), "📞 Bog'lanish & Aloqa", "📞 Контакты и Связь", "📞 Contact & Support"]:
        set_user_state(user.id, "NONE")
        await update.message.reply_text(
            t("contact_info", lang),
            reply_markup=get_main_reply_keyboard(lang),
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

    if text in [t("btn_lang", "uz"), t("btn_lang", "ru"), t("btn_lang", "en"), "🌐 Tilni o'zgartirish", "🌐 Сменить язык", "🌐 Change Language"]:
        set_user_state(user.id, "NONE")
        await update.message.reply_text(
            t("choose_lang", lang),
            reply_markup=get_language_keyboard(),
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown"
        )
        return

    # 2. Intelligent MAP & LOCATION Pin Trigger (Native Telegram Venue)
    detected_city_id = detect_city_in_text(text)
    is_loc = is_location_request(text)

    # A. If user asked about a specific city OR asking for map of that city
    if detected_city_id:
        target_id = detected_city_id
        set_user_state(user.id, state="NONE", last_center_id=target_id)
        center = TEST_CENTERS.get(target_id)
        if center:
            address = center.get(f"address_{lang}", center["address_uz"])
            # Send the interactive Telegram Venue Map Pin!
            await context.bot.send_venue(
                chat_id=update.message.chat_id,
                latitude=center["latitude"],
                longitude=center["longitude"],
                title=center["title"],
                address=address,
                reply_to_message_id=update.message.message_id
            )
            short_info = f"📍 *{center['title']}* lokatsiyasi yuborildi!\n\n📞 Tel: `{center['phone']}`\n⏰ Ish vaqti: {center['work_hours']}\n_Ushbu lokatsiyani bosib Google Maps yoki Yandex Go orqali to'g'ridan-to'g'ri marshrut chizishingiz mumkin._" if lang == "uz" else (
                f"📍 Локация *{center['title']}* отправлена!\n\n📞 Тел: `{center['phone']}`\n⏰ Время работы: {center['work_hours']}\n_Нажмите на карту выше для построения маршрута в Яндекс Картах или Google Maps._" if lang == "ru" else
                f"📍 Venue pin for *{center['title']}* has been sent!\n\n📞 Phone: `{center['phone']}`\n⏰ Hours: {center['work_hours']}\n_Tap the map above to navigate via Google Maps or Apple Maps._"
            )
            await update.message.reply_text(
                short_info,
                reply_markup=get_center_detail_keyboard(target_id, lang),
                parse_mode="Markdown"
            )
            return

    # B. If user asked "mapda korsat" / "show on map" without naming a city:
    if is_loc and ("map" in text.lower() or "karta" in text.lower() or "xarita" in text.lower() or "lokatsiya" in text.lower()):
        target_id = last_center_id or "tashkent_ciu"
        center = TEST_CENTERS.get(target_id, TEST_CENTERS["tashkent_ciu"])
        address = center.get(f"address_{lang}", center["address_uz"])
        await context.bot.send_venue(
            chat_id=update.message.chat_id,
            latitude=center["latitude"],
            longitude=center["longitude"],
            title=center["title"],
            address=address,
            reply_to_message_id=update.message.message_id
        )
        msg_text = f"📍 *{center['title']}* xaritasi!\n\nBoshqa shaharlar lokatsiyasini ko'rish uchun quyidagi tugmalardan foydalanishingiz mumkin:" if lang == "uz" else (
            f"📍 Карта для *{center['title']}*!\n\nДля выбора других городов воспользуйтесь кнопками ниже:" if lang == "ru" else
            f"📍 Map venue for *{center['title']}*!\n\nTo view other cities, use the buttons below:"
        )
        await update.message.reply_text(
            msg_text,
            reply_markup=get_regions_inline_keyboard(lang),
            parse_mode="Markdown"
        )
        return

    # 3. State: AWAITING_CALC_INPUT
    if state == "AWAITING_CALC_INPUT":
        if calc_mode == "overall":
            parts = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", text)
            if len(parts) >= 4:
                try:
                    scores = [float(p) for p in parts[:4]]
                    if all(0.0 <= s <= 9.0 for s in scores):
                        set_user_state(user.id, "NONE")
                        l, r, w, s = scores
                        avg, overall = calculate_overall_band(l, r, w, s)
                        feedback = get_band_feedback(overall, lang)
                        
                        resp = f"""🎯 *Overall Band Natijasi:*

🎧 Listening: `{l}`
📖 Reading: `{r}`
✍️ Writing: `{w}`
🗣 Speaking: `{s}`

━━━━━━━━━━━━━━━━━━━━
📈 *O'rtacha arifmetik:* `{avg}`
⭐ *Yakuniy Overall Band:* `{overall:.1f}`
━━━━━━━━━━━━━━━━━━━━

{feedback}""" if lang == "uz" else (
    f"""🎯 *Результат Overall Band:*

🎧 Listening: `{l}`
📖 Reading: `{r}`
✍️ Writing: `{w}`
🗣 Speaking: `{s}`

━━━━━━━━━━━━━━━━━━━━
📈 *Среднее арифметическое:* `{avg}`
⭐ *Итоговый Overall Band:* `{overall:.1f}`
━━━━━━━━━━━━━━━━━━━━

{feedback}""" if lang == "ru" else
    f"""🎯 *Overall Band Result:*

🎧 Listening: `{l}`
📖 Reading: `{r}`
✍️ Writing: `{w}`
🗣 Speaking: `{s}`

━━━━━━━━━━━━━━━━━━━━
📈 *Exact Average:* `{avg}`
⭐ *Final Overall Band:* `{overall:.1f}`
━━━━━━━━━━━━━━━━━━━━

{feedback}"""
)
                        await update.message.reply_text(
                            resp,
                            reply_markup=get_calculator_menu_keyboard(lang),
                            reply_to_message_id=update.message.message_id,
                            parse_mode="Markdown"
                        )
                        return
                except Exception:
                    pass
            await update.message.reply_text(
                t("invalid_overall", lang),
                reply_to_message_id=update.message.message_id,
                parse_mode="Markdown"
            )
            return
        else:
            if text.isdigit():
                raw = int(text)
                if 0 <= raw <= 40:
                    set_user_state(user.id, "NONE")
                    if calc_mode == "listening":
                        band = get_listening_band(raw)
                        module_title = "Listening"
                    elif calc_mode == "reading_acad":
                        band = get_academic_reading_band(raw)
                        module_title = "Reading Academic"
                    else:
                        band = get_general_reading_band(raw)
                        module_title = "Reading General"

                    feedback = get_band_feedback(band, lang)
                    
                    resp = f"""📊 *{module_title} Band Natijasi:*

✅ *To'g'ri javoblar:* `{raw} / 40`
⭐ *IELTS Band Ball:* `{band:.1f}`

{feedback}""" if lang == "uz" else (
    f"""📊 *Результат {module_title}:*

✅ *Правильных ответов:* `{raw} / 40`
⭐ *Балл IELTS Band:* `{band:.1f}`

{feedback}""" if lang == "ru" else
    f"""📊 *{module_title} Band Result:*

✅ *Raw Score:* `{raw} / 40`
⭐ *IELTS Band Score:* `{band:.1f}`

{feedback}"""
)
                    await update.message.reply_text(
                        resp,
                        reply_markup=get_calculator_menu_keyboard(lang),
                        reply_to_message_id=update.message.message_id,
                        parse_mode="Markdown"
                    )
                    return
            await update.message.reply_text(
                t("invalid_number", lang),
                reply_to_message_id=update.message.message_id,
                parse_mode="Markdown"
            )
            return

    # 4. Direct raw score conversion if user types only a single number
    if text.isdigit() and 0 <= int(text) <= 40:
        raw = int(text)
        l_band = get_listening_band(raw)
        r_acad = get_academic_reading_band(raw)
        r_gen = get_general_reading_band(raw)
        
        resp = f"""📊 *{raw} ta to'g'ri javob uchun IELTS ballari:*

🎧 *Listening:* `{l_band:.1f}`
📖 *Reading Academic:* `{r_acad:.1f}`
📰 *Reading General:* `{r_gen:.1f}`""" if lang == "uz" else (
    f"""📊 *Баллы IELTS для {raw} правильных ответов:*

🎧 *Listening:* `{l_band:.1f}`
📖 *Reading Academic:* `{r_acad:.1f}`
📰 *Reading General:* `{r_gen:.1f}`""" if lang == "ru" else
    f"""📊 *IELTS Scores for {raw} correct answers:*

🎧 *Listening:* `{l_band:.1f}`
📖 *Reading Academic:* `{r_acad:.1f}`
📰 *Reading General:* `{r_gen:.1f}`"""
)
        await update.message.reply_text(
            resp,
            reply_markup=get_calculator_menu_keyboard(lang),
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown"
        )
        return

    # 5. Intelligent AI Chat Response (Conversational, IELTS Expertise, Real-Time facts, Multi-turn Context)
    ai_response = await generate_ai_chat_response(
        user_id=user.id,
        user_text=text,
        user_name=user.first_name or "Candidate",
        lang=lang
    )

    try:
        await update.message.reply_text(
            ai_response,
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    except Exception:
        await update.message.reply_text(
            ai_response,
            reply_to_message_id=update.message.message_id,
            disable_web_page_preview=True
        )

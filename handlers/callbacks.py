"""
Inline callback query handlers for interactive features, quizzes, speaking simulator,
flashcards, region explorer, and band calculators.
"""
from telegram import Update
from telegram.ext import ContextTypes
from services.user_state import get_user_language, set_user_language, set_user_state
from locales import t
from data.test_centers import TEST_CENTERS
from data.interactive_content import QUIZ_QUESTIONS, SPEAKING_CUE_CARDS, BAND9_FLASHCARDS, REGION_CENTERS
from data.ielts_knowledge import COMPARISON_INFO
from keyboards import (
    get_main_reply_keyboard,
    get_regions_inline_keyboard,
    get_region_centers_keyboard,
    get_center_detail_keyboard,
    get_calculator_menu_keyboard,
    get_quiz_keyboard,
    get_speaking_cue_keyboard,
    get_flashcard_keyboard,
    get_retake_keyboard
)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    lang = get_user_language(user_id)

    # 1. Navigation Menus
    if data == "menu:main":
        set_user_state(user_id, "NONE")
        welcome_text = t("main_menu_title", lang)
        try:
            await query.message.edit_text(welcome_text, parse_mode="Markdown")
        except Exception:
            await query.message.reply_text(welcome_text, reply_markup=get_main_reply_keyboard(lang), parse_mode="Markdown")
        return

    if data == "menu:centers":
        set_user_state(user_id, "NONE")
        await query.message.edit_text(
            t("regions_title", lang),
            reply_markup=get_regions_inline_keyboard(lang),
            parse_mode="Markdown"
        )
        return

    # 2. Region & Test Centers
    if data.startswith("region:"):
        reg_key = data.split(":")[1]
        reg_data = REGION_CENTERS.get(reg_key)
        if reg_data:
            title = reg_data.get(f"title_{lang}", reg_data["title_uz"])
            msg_text = f"📍 *{title} IDP IELTS markazlari:*\n\nBatafsil ma'lumot olish yoki xaritada ko'rish uchun tanlang:" if lang=="uz" else (
                f"📍 *Центры IDP IELTS ({title}):*\n\nВыберите центр для просмотра информации и локации:" if lang=="ru" else
                f"📍 *IDP IELTS Centres in {title}:*\n\nSelect a centre for full details and map pin:"
            )
            await query.message.edit_text(
                msg_text,
                reply_markup=get_region_centers_keyboard(reg_key, lang),
                parse_mode="Markdown"
            )
        return

    if data.startswith("center:"):
        center_id = data.split(":")[1]
        center = TEST_CENTERS.get(center_id)
        if center:
            title = center["title"]
            address = center.get(f"address_{lang}", center["address_uz"])
            types = center.get(f"type_{lang}", center["type_uz"])
            phone = center["phone"]
            work_hours = center["work_hours"]

            text = t(
                "center_detail_template",
                lang,
                title=title,
                address=address,
                phone=phone,
                work_hours=work_hours,
                types=types
            )
            await query.message.edit_text(
                text,
                reply_markup=get_center_detail_keyboard(center_id, lang),
                parse_mode="Markdown"
            )
        return

    # 3. Send Venue / Map Location
    if data.startswith("venue:"):
        center_id = data.split(":")[1]
        center = TEST_CENTERS.get(center_id)
        if center:
            address = center.get(f"address_{lang}", center["address_uz"])
            await context.bot.send_venue(
                chat_id=query.message.chat_id,
                latitude=center["latitude"],
                longitude=center["longitude"],
                title=center["title"],
                address=address,
                reply_to_message_id=query.message.message_id
            )
            
            nav_text = f"📍 *{center['title']}* lokatsiyasi yuborildi!\n_Google Maps, Yandex Go yoki Apple Maps orqali to'g'ridan-to'g'ri marshrut chizishingiz mumkin._" if lang == "uz" else (
                f"📍 Локация *{center['title']}* отправлена!\n_Вы можете проложить маршрут в Яндекс Картах или Google Maps._" if lang == "ru" else
                f"📍 GPS pin for *{center['title']}* sent!\n_Open directly in your navigation app._"
            )
            await query.message.reply_text(nav_text, parse_mode="Markdown")
        return

    # 4. Interactive Quiz
    if data.startswith("quiz_show:"):
        qid = int(data.split(":")[1])
        q_data = next((q for q in QUIZ_QUESTIONS if q["id"] == qid), QUIZ_QUESTIONS[0])
        q_text = q_data.get(f"question_{lang}", q_data["question_uz"])
        opts = "\n".join(q_data["options"])
        full_text = f"{q_text}\n\n{opts}\n\n👇 *Variantlardan birini tanlang:*"
        await query.message.edit_text(
            full_text,
            reply_markup=get_quiz_keyboard(qid, lang=lang),
            parse_mode="Markdown"
        )
        return

    if data.startswith("quiz_ans:"):
        parts = data.split(":")
        qid = int(parts[1])
        chosen_opt = int(parts[2])
        q_data = next((q for q in QUIZ_QUESTIONS if q["id"] == qid), QUIZ_QUESTIONS[0])
        
        is_correct = (chosen_opt == q_data["correct"])
        q_text = q_data.get(f"question_{lang}", q_data["question_uz"])
        explanation = q_data.get(f"explanation_{lang}", q_data["explanation_uz"])
        
        result_header = "🎉 *BARAKALLA! TO'G'RI JAVOB!*" if is_correct else "❌ *NOTO'G'RI JAVOB!*"
        full_text = f"{result_header}\n\n{q_text}\n\n━━━━━━━━━━━━━━━━━━━━\n{explanation}"
        
        await query.message.edit_text(
            full_text,
            reply_markup=get_quiz_keyboard(qid, selected_opt=chosen_opt, is_answered=True, lang=lang),
            parse_mode="Markdown"
        )
        return

    # 5. Speaking Part 2 Simulator
    if data.startswith("speaking_show:"):
        cid = int(data.split(":")[1])
        card = next((c for c in SPEAKING_CUE_CARDS if c["id"] == cid), SPEAKING_CUE_CARDS[0])
        cues_text = "\n".join([f"• {c}" for c in card["cues"]])
        
        text = f"""🗣 *IELTS Speaking Part 2 Cue Card (#{card['id']}):*

📌 *Topic:* *{card['topic']}*

You should say:
{cues_text}

⏱ _Sizda reja tuzish uchun 1 daqiqa vaqt bor. So'ng 2 daqiqa davomida to'xtovsiz gapirishingiz kerak._"""
        await query.message.edit_text(
            text,
            reply_markup=get_speaking_cue_keyboard(cid, show_model=False, lang=lang),
            parse_mode="Markdown"
        )
        return

    if data.startswith("speaking_model:"):
        cid = int(data.split(":")[1])
        card = next((c for c in SPEAKING_CUE_CARDS if c["id"] == cid), SPEAKING_CUE_CARDS[0])
        vocab_text = "\n".join([f"⭐ *{v}*" for v in card["band9_vocab"]])
        
        text = f"""💡 *Band 9 Model Guide for Speaking Cue Card #{card['id']}:*

📌 *Topic:* _{card['topic']}_

🏆 *High-Scoring Band 9 Vocabulary & Idioms:*
{vocab_text}

📐 *Optimal Response Structure:*
{card['model_structure']}"""
        await query.message.edit_text(
            text,
            reply_markup=get_speaking_cue_keyboard(cid, show_model=True, lang=lang),
            parse_mode="Markdown"
        )
        return

    # 6. Band 9 Vocabulary Flashcards
    if data.startswith("flashcard:"):
        idx = int(data.split(":")[1])
        card = BAND9_FLASHCARDS[idx % len(BAND9_FLASHCARDS)]
        meaning = card.get(f"meaning_{lang}", card["meaning_uz"])
        
        text = f"""📚 *Band 9 Academic Vocabulary Flashcard ({idx+1}/{len(BAND9_FLASHCARDS)}):*

💎 *Word:* `{card['word']}`
🗣 *Pronunciation:* `{card['phonetic']}`
📖 *Meaning:* {meaning}
🔗 *Collocation:* `{card['collocation']}`

📝 *IELTS Example Sentence:*
_{card['ielts_sentence']}_"""
        await query.message.edit_text(
            text,
            reply_markup=get_flashcard_keyboard(idx, lang=lang),
            parse_mode="Markdown"
        )
        return

    # 7. Calculators
    if data.startswith("calc:"):
        mode = data.split(":")[1]
        if mode == "listening":
            set_user_state(user_id, "AWAITING_CALC_INPUT", "listening")
            await query.message.edit_text(
                t("calc_listening_prompt", lang),
                parse_mode="Markdown"
            )
        elif mode == "reading_acad":
            set_user_state(user_id, "AWAITING_CALC_INPUT", "reading_acad")
            await query.message.edit_text(
                t("calc_reading_acad_prompt", lang),
                parse_mode="Markdown"
            )
        elif mode == "reading_gen":
            set_user_state(user_id, "AWAITING_CALC_INPUT", "reading_gen")
            await query.message.edit_text(
                t("calc_reading_gen_prompt", lang),
                parse_mode="Markdown"
            )
        elif mode == "overall":
            set_user_state(user_id, "AWAITING_CALC_INPUT", "overall")
            await query.message.edit_text(
                t("calc_overall_prompt", lang),
                parse_mode="Markdown"
            )
        return

    # 8. Computer vs Paper Comparison
    if data == "retake:compare":
        comp_c = COMPARISON_INFO["computer"].get(lang, COMPARISON_INFO["computer"]["uz"])
        comp_p = COMPARISON_INFO["paper"].get(lang, COMPARISON_INFO["paper"]["uz"])
        full_comp = f"{comp_c}\n\n━━━━━━━━━━━━━━━━━━━━\n\n{comp_p}"
        await query.message.edit_text(
            full_comp,
            reply_markup=get_retake_keyboard(lang),
            parse_mode="Markdown"
        )
        return

    # 9. Language Switcher
    if data.startswith("lang:"):
        new_lang = data.split(":")[1]
        set_user_language(user_id, new_lang, query.from_user.username, query.from_user.first_name)
        msg_text = t("lang_changed", new_lang)
        await query.message.edit_text(msg_text, parse_mode="Markdown")
        await query.message.reply_text(
            t("main_menu_title", new_lang),
            reply_markup=get_main_reply_keyboard(new_lang),
            parse_mode="Markdown"
        )
        return

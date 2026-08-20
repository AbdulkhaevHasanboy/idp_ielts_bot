"""
Dynamic, engaging, and interactive keyboard builders for IDP IELTS Bot.
"""
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from locales import t
from data.test_centers import TEST_CENTERS
from data.interactive_content import REGION_CENTERS, QUIZ_QUESTIONS, SPEAKING_CUE_CARDS, BAND9_FLASHCARDS
from config import IDP_BOOKING_URL, IDP_OSR_URL

def get_main_reply_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(t("btn_centers", lang)), KeyboardButton(t("btn_quiz", lang))],
        [KeyboardButton(t("btn_speaking_sim", lang)), KeyboardButton(t("btn_flashcards", lang))],
        [KeyboardButton(t("btn_calculator", lang)), KeyboardButton(t("btn_register", lang))],
        [KeyboardButton(t("btn_retake", lang)), KeyboardButton(t("btn_contact", lang))],
        [KeyboardButton(t("btn_lang", lang))]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 1. Test Centres & Regions
def get_regions_inline_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    buttons = []
    for reg_key, data in REGION_CENTERS.items():
        title = data.get(f"title_{lang}", data["title_uz"])
        buttons.append([InlineKeyboardButton(title, callback_data=f"region:{reg_key}")])
    
    buttons.append([InlineKeyboardButton("🌐 Rasmiy saytdan joy band qilish (ielts.idp.com)", url=IDP_BOOKING_URL)])
    buttons.append([InlineKeyboardButton(t("btn_back_main", lang), callback_data="menu:main")])
    return InlineKeyboardMarkup(buttons)

def get_region_centers_keyboard(region_key: str, lang: str = "uz") -> InlineKeyboardMarkup:
    region = REGION_CENTERS.get(region_key)
    buttons = []
    if region:
        for cid in region["centers"]:
            cdata = TEST_CENTERS.get(cid)
            if cdata:
                cname = cdata.get(f"city_{lang}", cdata["city_uz"])
                buttons.append([
                    InlineKeyboardButton(f"🏛 {cname}", callback_data=f"center:{cid}"),
                    InlineKeyboardButton("📍 Xarita", callback_data=f"venue:{cid}")
                ])
    buttons.append([InlineKeyboardButton("◀️ Boshqa hududlar" if lang=="uz" else ("◀️ Другие регионы" if lang=="ru" else "◀️ Other regions"), callback_data="menu:centers")])
    buttons.append([InlineKeyboardButton(t("btn_back_main", lang), callback_data="menu:main")])
    return InlineKeyboardMarkup(buttons)

def get_center_detail_keyboard(center_id: str, lang: str = "uz") -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(t("btn_send_venue", lang), callback_data=f"venue:{center_id}")],
        [InlineKeyboardButton("🔗 Saytdan joy band qilish (Book Test)", url=IDP_BOOKING_URL)],
        [InlineKeyboardButton(t("btn_back_centers", lang), callback_data="menu:centers")]
    ]
    return InlineKeyboardMarkup(buttons)

# 2. Interactive Daily IELTS Quiz Keyboards
def get_quiz_keyboard(question_id: int, selected_opt: int = None, is_answered: bool = False, lang: str = "uz") -> InlineKeyboardMarkup:
    q_data = next((q for q in QUIZ_QUESTIONS if q["id"] == question_id), QUIZ_QUESTIONS[0])
    buttons = []

    if not is_answered:
        # Show options A, B, C, D
        row1 = [
            InlineKeyboardButton("A", callback_data=f"quiz_ans:{question_id}:0"),
            InlineKeyboardButton("B", callback_data=f"quiz_ans:{question_id}:1")
        ]
        row2 = [
            InlineKeyboardButton("C", callback_data=f"quiz_ans:{question_id}:2"),
            InlineKeyboardButton("D", callback_data=f"quiz_ans:{question_id}:3")
        ]
        buttons.append(row1)
        buttons.append(row2)
    else:
        # After answer
        next_id = (question_id % len(QUIZ_QUESTIONS)) + 1
        buttons.append([InlineKeyboardButton("🔄 Keyingi savol (Next Question) ➡️", callback_data=f"quiz_show:{next_id}")])

    buttons.append([InlineKeyboardButton(t("btn_back_main", lang), callback_data="menu:main")])
    return InlineKeyboardMarkup(buttons)

# 3. Speaking Part 2 Simulator Keyboard
def get_speaking_cue_keyboard(card_id: int, show_model: bool = False, lang: str = "uz") -> InlineKeyboardMarkup:
    next_id = (card_id % len(SPEAKING_CUE_CARDS)) + 1
    buttons = []
    
    if not show_model:
        buttons.append([InlineKeyboardButton("💡 Band 9 Model Javob & So'zlar", callback_data=f"speaking_model:{card_id}")])
    
    buttons.append([InlineKeyboardButton("🔄 Boshqa mavzu (Next Cue Card) ➡️", callback_data=f"speaking_show:{next_id}")])
    buttons.append([InlineKeyboardButton(t("btn_back_main", lang), callback_data="menu:main")])
    return InlineKeyboardMarkup(buttons)

# 4. Band 9 Vocabulary Flashcards Keyboard
def get_flashcard_keyboard(card_idx: int, lang: str = "uz") -> InlineKeyboardMarkup:
    next_idx = (card_idx + 1) % len(BAND9_FLASHCARDS)
    buttons = [
        [InlineKeyboardButton("🔄 Keyingi so'z (Next Word) ➡️", callback_data=f"flashcard:{next_idx}")],
        [InlineKeyboardButton(t("btn_back_main", lang), callback_data="menu:main")]
    ]
    return InlineKeyboardMarkup(buttons)

# 5. Calculator Keyboard
def get_calculator_menu_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(t("btn_calc_listening", lang), callback_data="calc:listening"),
            InlineKeyboardButton(t("btn_calc_overall", lang), callback_data="calc:overall")
        ],
        [
            InlineKeyboardButton(t("btn_calc_reading_acad", lang), callback_data="calc:reading_acad"),
            InlineKeyboardButton(t("btn_calc_reading_gen", lang), callback_data="calc:reading_gen")
        ],
        [InlineKeyboardButton(t("btn_back_main", lang), callback_data="menu:main")]
    ]
    return InlineKeyboardMarkup(buttons)

# 6. Retake Keyboard
def get_retake_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("💻 Computer vs Paper farqlari" if lang=="uz" else ("💻 Различия Computer vs Paper" if lang=="ru" else "💻 Computer vs Paper comparison"), callback_data="retake:compare")],
        [InlineKeyboardButton("🔗 OSR Rasmiy sahifasi (IDP)", url=IDP_OSR_URL)],
        [InlineKeyboardButton(t("btn_back_main", lang), callback_data="menu:main")]
    ]
    return InlineKeyboardMarkup(buttons)

# 7. Language Switcher
def get_language_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang:uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang:en")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

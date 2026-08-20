"""
Interactive data for dynamic IELTS quizzes, Speaking Part 2 simulators, and Band 9 flashcards.
"""

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question_uz": "🧩 *IELTS Vocabulary Challenge:*\n\nQaysi so'z 'muammoni yanada og'irlashtirmoq, yomonlashtirmoq' ma'nosini bildiradi va IELTS Writing Task 2 da yuqori ball olib keladi?",
        "question_ru": "🧩 *IELTS Vocabulary Challenge:*\n\nКакое слово означает 'усугублять, ухудшать проблему' и используется в академическом IELTS Writing Task 2?",
        "question_en": "🧩 *IELTS Vocabulary Challenge:*\n\nWhich academic word means 'to make a problem or bad situation worse' and boosts your Lexical Resource in Writing Task 2?",
        "options": ["A) Alleviate", "B) Exacerbate", "C) Reconcile", "D) Proliferate"],
        "correct": 1, # B) Exacerbate
        "explanation_uz": "✅ *To'g'ri javob: B) Exacerbate*\n\n📌 *Ma'nosi:* Muammoni yanada kuchaytirish / yomonlashtirish (to aggravate / worsen).\n📝 *Misol:* _'Rapid urbanisation can exacerbate traffic congestion in major cities.'_\n\n⚠️ *Alleviate* esa aksincha 'yengillashtirmoq' degani.",
        "explanation_ru": "✅ *Правильный ответ: B) Exacerbate*\n\n📌 *Значение:* Усугублять, ухудшать ситуацию.\n📝 *Пример:* _'Rapid urbanisation can exacerbate traffic congestion in major cities.'_\n\n⚠️ *Alleviate* означает противоположное — 'облегчать'.",
        "explanation_en": "✅ *Correct Answer: B) Exacerbate*\n\n📌 *Meaning:* To make something that is already bad even worse.\n📝 *Example:* _'Rapid urbanisation can exacerbate traffic congestion in major cities.'_\n\n⚠️ *Alleviate* means the opposite ('to make less severe')."
    },
    {
        "id": 2,
        "question_uz": "✍️ *IELTS Writing Task 2 Qoidasi:*\n\nTask 2 esseda eng kamida nechta so'z yozish talab qilinadi?",
        "question_ru": "✍️ *Правило IELTS Writing Task 2:*\n\nКакое минимальное количество слов необходимо написать в эссе Task 2?",
        "question_en": "✍️ *IELTS Writing Task 2 Rule:*\n\nWhat is the minimum recommended word count for IELTS Writing Task 2?",
        "options": ["A) 150 so'z", "B) 200 so'z", "C) 250 so'z", "D) 300 so'z"],
        "correct": 2, # C) 250
        "explanation_uz": "✅ *To'g'ri javob: C) 250 so'z*\n\n📌 Task 2 uchun minimal talab — *250 ta so'z*. Agar 250 dan kam so'z yozilsa, Task Achievement mezonidan ball tushiriladi. Tavsiya etilgan optimal hajm: *260 - 280 so'z*.",
        "explanation_ru": "✅ *Правильный ответ: C) 250 слов*\n\n📌 Минимальный порог для Task 2 — *250 слов*. Если слов меньше, снижается балл за Task Achievement. Оптимальный объем: *260 - 280 слов*.",
        "explanation_en": "✅ *Correct Answer: C) 250 words*\n\n📌 The official minimum for Task 2 is *250 words*. Writing fewer words leads to an automatic penalty in Task Achievement. The sweet spot is *260–280 words*."
    },
    {
        "id": 3,
        "question_uz": "🎧 *IELTS Listening Trap (Tuzoq):*\n\nListening testida gapiruvchi avval bir sanani aytib, keyin *'Actually, wait, my flight got rescheduled to Friday'* desa, qaysi javob olinadi?",
        "question_ru": "🎧 *Ловушка в IELTS Listening:*\n\nЕсли спикер сначала назвал одну дату, а затем сказал *'Actually, wait, my flight got rescheduled to Friday'*, какой ответ правильный?",
        "question_en": "🎧 *IELTS Listening Distractor Trap:*\n\nWhen a speaker mentions a date but corrects themselves with *'Actually, wait, my flight got rescheduled to Friday'*, which answer is correct?",
        "options": ["A) Birinchi aytilgan sana", "B) Oxirgi tuzatilgan sana (Friday)", "C) Ikkala sana ham", "D) Hech qaysisi"],
        "correct": 1, # B)
        "explanation_uz": "✅ *To'g'ri javob: B) Oxirgi tuzatilgan sana (Friday)*\n\n📌 Bu IELTS Listeningdagi eng mashhur 'Distractor / Self-correction' tuzog'i hisoblanadi. Har doim gapiruvchining tuzatish kiritgan yakuniy ma'lumotiga e'tibor bering!",
        "explanation_ru": "✅ *Правильный ответ: B) Последняя исправленная дата (Friday)*\n\n📌 Это классический прием 'Distractor' в Listening. Экзаменаторы специально называют ложный ответ, а затем исправляют его.",
        "explanation_en": "✅ *Correct Answer: B) The corrected final date (Friday)*\n\n📌 This is the classic self-correction distractor in IELTS Listening. Always look out for keywords like *'actually, wait, no, instead'*."
    },
    {
        "id": 4,
        "question_uz": "📖 *IELTS Reading: True / False / Not Given:*\n\nMatnda: *'The company made record profits in 2024.'* deyilgan bo'lsa, Savolda: *'The company is the most profitable in Europe.'* deyilgan bo'lsa, javob nima bo'ladi?",
        "question_ru": "📖 *IELTS Reading: True / False / Not Given:*\n\nВ тексте: *'The company made record profits in 2024.'* Вопрос: *'The company is the most profitable in Europe.'* Какой ответ?",
        "question_en": "📖 *IELTS Reading: True / False / Not Given:*\n\nText: *'The company made record profits in 2024.'* Statement: *'The company is the most profitable in Europe.'* What is the answer?",
        "options": ["A) TRUE", "B) FALSE", "C) NOT GIVEN", "D) CANNOT BE DETERMINED"],
        "correct": 2, # C) NOT GIVEN
        "explanation_uz": "✅ *To'g'ri javob: C) NOT GIVEN*\n\n📌 Kompaniya rekord darajada foyda ko'rgani aytilgan, ammo butun Yevropada eng ko'p foyda ko'rgan kompaniyami yoki yo'qmi — bu haqda ma'lumot yo'q!",
        "explanation_ru": "✅ *Правильный ответ: C) NOT GIVEN*\n\n📌 В тексте говорится о рекордной прибыли компании, но нет сравнения с другими компаниями Европы.",
        "explanation_en": "✅ *Correct Answer: C) NOT GIVEN*\n\n📌 While the text confirms record profits, it does NOT provide any comparative information about other companies in Europe."
    }
]

SPEAKING_CUE_CARDS = [
    {
        "id": 1,
        "topic": "Describe an important decision you made in your life",
        "cues": [
            "What the decision was",
            "When you made it",
            "How you made this decision",
            "And explain why this decision was so important for your future"
        ],
        "band9_vocab": [
            "Life-altering choice (hayotni o'zgartiruvchi tanlov)",
            "Crossroads (chorraha / muhim palla)",
            "Weigh up the pros and cons (foyda va zararlarini taroziga solmoq)",
            "Pivotal milestone (hal qiluvchi bosqich)",
            "Hindsight (o'tmishga nazar)"
        ],
        "model_structure": "1. Introduction: Set the scene (e.g. After graduating from high school...)\n2. Context & Options: What were the alternatives?\n3. Decision-making process: Who did you consult? (mentors, parents)\n4. Outcome & Reflection: How it shaped your personality today."
    },
    {
        "id": 2,
        "topic": "Describe a piece of technology that you find difficult to live without",
        "cues": [
            "What it is and when you got it",
            "How often you use it",
            "What you mainly use it for",
            "And explain why it is indispensable to your daily routine"
        ],
        "band9_vocab": [
            "Indispensable / Ubiquitous (ajralmas / har yerda bor)",
            "Streamline daily workflow (kunlik ishni osonlashtirmoq)",
            "Cutting-edge features (eng zamonaviy funksiyalar)",
            "Technological dependency (texnologiyaga qaramlik)",
            "Boost productivity exponentially (samaradorlikni bir necha barobar oshirmoq)"
        ],
        "model_structure": "1. Paraphrase & Introduction: Name the device (e.g. tablet / noise-canceling headphones).\n2. Daily application: Study, communication, time management.\n3. Contrast: How life was before having this technology.\n4. Summary: Why modern life necessitates it."
    },
    {
        "id": 3,
        "topic": "Describe a place in your city where you enjoy relaxing",
        "cues": [
            "Where this place is located",
            "What it looks like",
            "How often you visit it",
            "And explain why it helps you unwind and recharge"
        ],
        "band9_vocab": [
            "Tranquil oasis (tinch, osoyishta maskan)",
            "Bustle and hustle of urban life (shahar shovqin-suroni)",
            "Unwind and decompress (dam olmoq va xordiq chiqarmoq)",
            "Picturesque surroundings (ko'rkam, manzarali tevarak-atrof)",
            "Rejuvenate one's mind (ongni yangilamoq, tetiklashtirmoq)"
        ],
        "model_structure": "1. Location & Setting: Name the park/cafe in Tashkent/Samarkand.\n2. Atmosphere & Sensory details: Sounds of nature, architecture, greenery.\n3. Personal ritual: Reading, walking, listening to podcasts.\n4. Emotional value: Contrast with stressful work/study routine."
    }
]

BAND9_FLASHCARDS = [
    {
        "word": "Ubiquitous (adj)",
        "phonetic": "/juːˈbɪk.wə.təs/",
        "meaning_uz": "Hamma joyda uchraydigan, keng tarqalgan",
        "meaning_ru": "Вездесущий, повсеместный",
        "meaning_en": "Present, appearing, or found everywhere",
        "collocation": "ubiquitous presence / ubiquitous technology",
        "ielts_sentence": "Smartphones have become ubiquitous across modern society, reshaping interpersonal communication."
    },
    {
        "word": "Detrimental (adj)",
        "phonetic": "/ˌdet.rəˈmen.təl/",
        "meaning_uz": "Zararli, salbiy ta'sir ko'rsatuvchi",
        "meaning_ru": "Пагубный, вредный, наносящий ущерб",
        "meaning_en": "Tending to cause harm or damage",
        "collocation": "detrimental effect / highly detrimental",
        "ielts_sentence": "Sedentary lifestyle habits have a detrimental effect on cardiovascular health and overall well-being."
    },
    {
        "word": "Mitigate (verb)",
        "phonetic": "/ˈmɪt.ə.ɡeɪt/",
        "meaning_uz": "Kamaytirmoq, yumshatmoq, yengillashtirmoq",
        "meaning_ru": "Смягчать, уменьшать последствия",
        "meaning_en": "Make something less severe, serious, or painful",
        "collocation": "mitigate the impact / mitigate risks",
        "ielts_sentence": "Governments must invest heavily in renewable energy to mitigate the adverse effects of global warming."
    },
    {
        "word": "Plausible (adj)",
        "phonetic": "/ˈplɑː.zə.bəl/",
        "meaning_uz": "Haqiqatga yaqin, asosli, ishonarli",
        "meaning_ru": "Правдоподобный, убедительный",
        "meaning_en": "Seeming reasonable or probable",
        "collocation": "plausible explanation / plausible scenario",
        "ielts_sentence": "Scientists have proposed a plausible explanation for the sudden shifts in regional climate patterns."
    }
]

REGION_CENTERS = {
    "tashkent": {
        "title_uz": "🏛 Toshkent shahri",
        "title_ru": "🏛 Город Ташкент",
        "title_en": "🏛 Tashkent City",
        "centers": ["tashkent_ciu", "tashkent_afrosiyob"]
    },
    "valley": {
        "title_uz": "🌄 Farg'ona vodiysi",
        "title_ru": "🌄 Ферганская долина",
        "title_en": "🌄 Fergana Valley",
        "centers": ["fergana", "namangan", "andijan"]
    },
    "sam_bukh": {
        "title_uz": "🕌 Samarqand & Buxoro",
        "title_ru": "🕌 Самарканд и Бухара",
        "title_en": "🕌 Samarkand & Bukhara",
        "centers": ["samarkand", "bukhara"]
    },
    "south": {
        "title_uz": "🌴 Janubiy hududlar",
        "title_ru": "🌴 Южные регионы",
        "title_en": "🌴 Southern Regions",
        "centers": ["navoi", "termez"]
    },
    "west": {
        "title_uz": "🌊 Qoraqalpog'iston & Xorazm",
        "title_ru": "🌊 Каракалпакстан и Хорезм",
        "title_en": "🌊 Karakalpakstan & Khorezm",
        "centers": ["urgench", "nukus"]
    }
}

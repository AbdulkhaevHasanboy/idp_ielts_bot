"""
IELTS Knowledge base, conversion tables, One Skill Retake, and test preparation resources for IDP IELTS in Uzbekistan.
"""

# Score Conversion Tables (0-40 correct answers to Band Score)
LISTENING_SCORES = {
    (39, 40): 9.0,
    (37, 38): 8.5,
    (35, 36): 8.0,
    (32, 34): 7.5,
    (30, 31): 7.0,
    (26, 29): 6.5,
    (23, 25): 6.0,
    (18, 22): 5.5,
    (16, 17): 5.0,
    (13, 15): 4.5,
    (10, 12): 4.0,
    (8, 9): 3.5,
    (6, 7): 3.0,
    (4, 5): 2.5,
    (0, 3): 2.0
}

READING_ACADEMIC_SCORES = {
    (39, 40): 9.0,
    (37, 38): 8.5,
    (35, 36): 8.0,
    (33, 34): 7.5,
    (30, 32): 7.0,
    (27, 29): 6.5,
    (23, 26): 6.0,
    (19, 22): 5.5,
    (15, 18): 5.0,
    (13, 14): 4.5,
    (10, 12): 4.0,
    (8, 9): 3.5,
    (6, 7): 3.0,
    (4, 5): 2.5,
    (0, 3): 2.0
}

READING_GENERAL_SCORES = {
    (40, 40): 9.0,
    (39, 39): 8.5,
    (37, 38): 8.0,
    (36, 36): 7.5,
    (34, 35): 7.0,
    (32, 33): 6.5,
    (30, 31): 6.0,
    (27, 29): 5.5,
    (23, 26): 5.0,
    (19, 22): 4.5,
    (15, 18): 4.0,
    (12, 14): 3.5,
    (9, 11): 3.0,
    (6, 8): 2.5,
    (0, 5): 2.0
}

CEFR_MAPPING = {
    "9.0": {"cefr": "C2", "level_uz": "Mukammal (Proficient)", "desc": "Tilni ona tilidek erkin va aniq bilish."},
    "8.5": {"cefr": "C2", "level_uz": "Mukammal (Very Good)", "desc": "Murakkab mavzularda erkin muloqot va tahlil."},
    "8.0": {"cefr": "C1/C2", "level_uz": "Juda yaxshi (Very Good)", "desc": "C1/C2 daraja. Xalqaro nufuzli universitetlar va stipendiyalar talabi."},
    "7.5": {"cefr": "C1", "level_uz": "Yaxshi (Good User)", "desc": "C1 daraja. O'zbekiston OTMlarida 100% maksimal ball (chet tili blokidan)."},
    "7.0": {"cefr": "C1", "level_uz": "Yaxshi (Good User)", "desc": "C1 daraja. Magistratura va chet el universitetlari uchun to'liq mos."},
    "6.5": {"cefr": "B2", "level_uz": "Mustaqil (Competent)", "desc": "B2 daraja. Bakalavr grantlari va ko'pchilik xalqaro dasturlar talabi."},
    "6.0": {"cefr": "B2", "level_uz": "Mustaqil (Competent)", "desc": "B2 daraja. O'zbekiston bakalavriatiga kirishda imtiyoz beradi."},
    "5.5": {"cefr": "B2/B1", "level_uz": "O'rta (Modest User)", "desc": "B2 boshlang'ich daraja."},
    "5.0": {"cefr": "B1", "level_uz": "Boshlang'ich mustaqil", "desc": "B1 daraja."},
}

# IDP IELTS Comparison: Computer vs Paper
COMPARISON_INFO = {
    "computer": {
        "uz": """💻 *IELTS on Computer (Kompyuterda IELTS):*
• *Natijalar tezligi:* 1 - 5 kun ichida chiqadi (juda tez!).
• *Qulaylik:* Shaxsiy kompyuter, zamonaviy quloqchinlar (headphones), klaviaturada yozish (Writingda so'zlarni avtomatik hisoblaydi va o'chirish/tahrirlash juda oson).
• *Test kunlari:* Toshkent va viloyatlarda deyarli har kuni, haftasiga 5-7 kun o'tkaziladi.
• *One Skill Retake (OSR):* Faqat kompyuterda topshirgan nomzodlar uchun amal qiladi! Agar biror moduldan past ball olsangiz, 60 kun ichida qayta topshirish imkoniyati bor.
• *Speaking:* Xuddi qog'ozdagi kabi jonli, sertifikatlangan imtihon oluvchi (examiner) bilan yuzma-yuz o'tkaziladi.""",
        "ru": """💻 *IELTS on Computer (IELTS на компьютере):*
• *Скорость результатов:* от 1 до 5 дней (очень быстро!).
• *Удобство:* Индивидуальный ПК, качественные наушники, счетчик слов в секции Writing, легкое редактирование текста.
• *Даты экзаменов:* Проводятся практически ежедневно в Ташкенте и регионах.
• *One Skill Retake (OSR):* Доступно ТОЛЬКО для тех, кто сдавал на компьютере! Возможность пересдать один модуль в течение 60 дней.
• *Speaking:* Проходит лицом к лицу с сертифицированным экзаменатором, как и в Paper-based.""",
        "en": """💻 *IELTS on Computer:*
• *Results delivery:* Fast turnaround in just 1 to 5 days!
• *Comfort:* Individual PC, noise-canceling headphones, automatic word counter in Writing, easy cut/paste editing.
• *Test Frequency:* Available almost every day of the week in Tashkent and regional centers.
• *One Skill Retake (OSR):* Exclusively available for computer-delivered tests! Retake any single component within 60 days.
• *Speaking:* Conducted face-to-face with a certified native IELTS examiner."""
    },
    "paper": {
        "uz": """📝 *IELTS on Paper (Qog'ozdagi an'anaviy IELTS):*
• *Natijalar tezligi:* Imtihondan so'ng 13-kuni chiqadi.
• *Format:* Savol daftarchasi va javob varaqasi (Answer Sheet). Qalam va o'chirg'ich bilan qo'lda yoziladi.
• *Listening:* Test oxirida javoblarni varaqaga ko'chirish uchun qo'shimcha 10 daqiqa vaqt beriladi.
• *Test kunlari:* Odatda oyiga 3-4 marta (asosan payshanba va shanba kunlari).
• *One Skill Retake:* Qog'ozdagi IELTS uchun One Skill Retake mavjud emas (barcha 4 modulni qayta topshirish kerak bo'ladi).""",
        "ru": """📝 *IELTS on Paper (Традиционный на бумаге):*
• *Скорость результатов:* На 13-й календарный день.
• *Формат:* Бумажный буклет с вопросами и бланки ответов (Answer Sheets). Письмо карандашом от руки.
• *Listening:* Предоставляется 10 дополнительных минут на перенос ответов в бланк.
• *Даты экзаменов:* Обычно 3-4 раза в месяц (по четвергам и субботам).
• *One Skill Retake:* Недоступно для бумажного формата.""",
        "en": """📝 *IELTS on Paper:*
• *Results delivery:* 13 calendar days after test day.
• *Format:* Paper booklets and answer sheets, handwritten with pencil.
• *Listening:* 10 extra transfer minutes at the end of the test.
• *Test Schedule:* Fixed dates 3-4 times a month (Thursdays & Saturdays).
• *One Skill Retake:* Not available for paper-based tests."""
    }
}

ONE_SKILL_RETAKE_INFO = {
    "uz": """🔄 *IDP IELTS One Skill Retake (OSR) nima va qanday ishlaydi?*

1. *Mohiyati:* Agar siz IELTS on Computer topshirgan bo'lsangiz va faqat bitta moduldan (masalan Writing yoki Speaking) kutilgan ballni ololmagan bo'lsangiz, barcha 4 ta modulni qayta topshirish shart emas! Faqat shu bitta modulni qaytadan topshirishingiz mumkin.
2. *Shartlari:*
   • Asosiy to'liq imtihon *IELTS on Computer* formatida topshirilgan bo'lishi kerak.
   • Asosiy imtihon sanasidan boshlab *60 kun* ichida OSR ga ro'yxatdan o'tish lozim.
   • Bitta to'liq test uchun faqat *1 marta* bitta modulni qayta topshirish mumkin.
3. *Sertifikat (TRF):* Sizga yangi Test Report Form beriladi, unda OSR moduli bo'yicha yangi ball va qolgan 3 ta modulning avvalgi ballari qayd etiladi.
4. *Qabul qilinishi:* Dunyoning 12,000 dan ortiq universitetlari va O'zbekiston OTMlari OSR sertifikatini rasman qabul qiladi.
5. *Narxi:* Taxminan 1,850,000 UZS.

📌 *Ro'yxatdan o'tish:* IDP IELTS shaxsiy kabinetingiz orqali (ielts.idp.com).""",
    "ru": """🔄 *IDP IELTS One Skill Retake (OSR) - Как это работает?*

1. *Суть:* Если вы сдали IELTS on Computer и вам не хватило баллов всего по одному навыку (например, Writing или Speaking), вам не нужно пересдавать весь экзамен! Вы можете пересдать только этот один модуль.
2. *Условия:*
   • Экзамен должен быть сдан в формате *IELTS on Computer*.
   • С момента сдачи основного теста должно пройти не более *60 дней*.
   • Пересдать можно только *один* компонент один раз на один полный экзамен.
3. *Сертификат (TRF):* Вы получаете новый обновленный сертификат TRF с новым баллом по пересданному модулю и сохраненными баллами по остальным.
4. *Признание:* Принимается более чем 12 000 учебных заведений по всему миру и вузами Узбекистана.
5. *Стоимость:* Около 1 850 000 сум.

📌 *Регистрация:* В личном кабинете на ielts.idp.com.""",
    "en": """🔄 *IDP IELTS One Skill Retake (OSR) Guide:*

1. *What is it:* If you took IELTS on Computer and didn't achieve your desired score in just one skill (Listening, Reading, Writing, or Speaking), you can retake that single skill without retaking the entire test!
2. *Eligibility:*
   • Must have taken *IELTS on Computer*.
   • Must register and take OSR within *60 days* of your original test date.
   • Can be used only *once* per full IELTS test sitting.
3. *New TRF:* You receive a new Test Report Form showing your updated score for the retaken skill alongside original scores for the other 3 skills.
4. *Recognition:* Recognized by over 12,000 organizations worldwide and higher education institutions in Uzbekistan.
5. *Fee:* Approx. 1,850,000 UZS.

📌 *Booking:* Directly via your IDP test taker portal at ielts.idp.com."""
}

PREPARATION_RESOURCES = {
    "uz": """📚 *IDP IELTS Tayyorgarlik va Bepul Materiallar:*

1. 💻 *IELTS on Computer Bepul Familiarisation Test:*
   Kompyuter formatidagi rasmiy simulyator. Test interfeysi, vaqtni boshqarish va vositalar bilan oldindan tanishing:
   🔗 [IDP Computer Familiarisation](https://ielts.idp.com/prepare/article-free-ielts-computer-delivered-practice-test)

2. 🎧 *IELTS by IDP App (Mobil ilova):*
   Rasmiy mobil ilovada bepul 400+ ta dars, amaliy testlar va band kalkulyatori mavjud (App Store va Google Play).

3. ✍️ *Writing Band 9 Maslahatlari:*
   • *Task 1:* Aniq kirish (paraphrase), umumiy umumlashtirish (Overall trend/overview) va 2 ta detallar paragrafi yozing. Hech qachon o'z fikringizni qo'shmang.
   • *Task 2:* 4 paragrafli struktura (Introduction + thesis, Body 1, Body 2, Conclusion). Har bir paragrafda 1 ta asosiy g'oya, tushuntirish va misol bering.

4. 🗣 *Speaking Maslahatlari:*
   • Tez emas, ravon va tabiiy gapiring.
   • Savolga to'g'ridan-to'g'ri javob bering va uni rivojlantiring (Why? Because...).
   • Examiner bilan ko'z bilan aloqa (eye-contact) qiling va savolni tushunmasangiz, muloyimlik bilan qaytarishini so'rang (*"Could you please rephrase that?"*).""",
    "ru": """📚 *Материалы для подготовки IDP IELTS:*

1. 💻 *Бесплатный симулятор IELTS on Computer:*
   Официальный тренажер интерфейса компьютерного теста:
   🔗 [IDP Computer Familiarisation](https://ielts.idp.com/prepare/article-free-ielts-computer-delivered-practice-test)

2. 🎧 *Приложение IELTS by IDP:*
   Официальное мобильное приложение с 400+ видеоуроками и практическими тестами.

3. ✍️ *Советы для секции Writing (Band 9):*
   • *Task 1:* Четкий парафраз задания, обязательный Overview (главные тренды) и 2 абзаца с цифрами/фактами.
   • *Task 2:* Структура из 4 абзацев (Введение с тезисом, Основная часть 1, Основная часть 2, Заключение).

4. 🗣 *Советы для Speaking:*
   • Говорите бегло и уверенно, не торопитесь.
   • Развивайте ответы с помощью примеров.
   • Если вопрос не понятен, вежливо переспросите (*"Could you rephrase the question, please?"*).""",
    "en": """📚 *IDP IELTS Preparation & Free Resources:*

1. 💻 *Official IELTS on Computer Familiarisation Test:*
   Experience the exact computer test interface before your exam day:
   🔗 [IDP Computer Familiarisation](https://ielts.idp.com/prepare/article-free-ielts-computer-delivered-practice-test)

2. 🎧 *IELTS by IDP App:*
   Download the official IDP prep app on iOS/Android for 400+ lessons, quizzes and webinars.

3. ✍️ *Writing Band 9 Core Strategies:*
   • *Task 1:* Clear paraphrase, compulsory clear OVERVIEW showing main trends, and 2 body paragraphs grouping data logically.
   • *Task 2:* 4-paragraph structure (Intro + direct thesis, Body 1 with Topic Sentence + Explanation + Example, Body 2, Conclusion).

4. 🗣 *Speaking Strategies:*
   • Focus on fluency, coherence, and natural pronunciation over overly complex jargon.
   • Extend your answers using reasons, examples, and personal experiences."""
}

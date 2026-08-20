# 🇺🇿 IDP IELTS Uzbekistan AI Telegram Bot

Rasmiy **IDP IELTS Uzbekistan** (Edu-Action) uchun ishlab chiqilgan, Sun'iy Intellekt (Gemini AI Vision & Chat), Telegram Native GPS Map/Venue integratsiyasi va interaktiv trenajyorlar bilan jihozlangan aqlli Telegram bot.

---

## 🌟 Asosiy Imkoniyatlar:

1. **🧠 Aqlli AI Murabbiy (Gemini 2.5 Flash):**
   - Nomzodlarning istalgan savollariga o'zbek, rus va ingliz tillarida tabiiy, aniq va tushunarli javob beradi.
   - Yangi faktik ma'lumotlar va yangiliklar so'ralganda fon rejimida mustaqil qidiruv (Silent Web Search) amalga oshiradi.

2. **👁 Multimodal AI Tahlil (Rasm, Insho va Hujjatlar):**
   - **IELTS Writing Essay:** Qo'lda yoki kompyuterda yozilgan insho rasmini tahlil qilib, 4 ta rasmiy mezon (*Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy*) bo'yicha baholaydi va Band 9 yaxshilash tavsiyalarini beradi.
   - **IELTS Savollari & Grafiklarni yechish:** Qiyin topshiriqlarni tushuntirib beradi.
   - **Noma'lum rasmlar (shtrix-kod, obyektlar):** Rasmni aniq aniqlab, nima qilish kerakligini tushuntiradi.

3. **🗺 Telegram Native GPS Lokatsiya / Venue:**
   - O'zbekistondagi barcha rasmiy test markazlari (Toshkent CIU, Toshkent Afrosiyob, Samarqand, Andijon, Farg'ona, Namangan, Buxoro, Urganch, Nukus, Navoiy, Termiz) uchun to'g'ridan-to'g'ri Telegram Xarita pinini (`send_venue`) yuboradi.
   - 1 marta bosish orqali Google Maps yoki Yandex Go orqali taksi chaqirish yoki marshrut chizish imkoniyati.

4. **🎯 Dinamik Interaktiv UI:**
   - **Kunlik Quiz (Challenge):** Imtihon tuzoqlari va grammatika/so'z boyligi bo'yicha interaktiv savol-javoblar.
   - **Speaking Part 2 Trenajyor:** 1 daqiqalik reja tuzish va Band 9 model javoblar.
   - **Band 9 So'z Boyligi:** Interaktiv kartochkalar (Flashcards).
   - **Band Score Kalkulyatori:** Listening, Reading (Academic & General) va Overall ballarni rasmiy yaxlitlash shkalasi bo'yicha hisoblash.

5. **👤 Inson Qo'llab-quvvatlash Xodimi:**
   - Telegram: [@idp555](https://t.me/idp555)
   - Call Centre: `+998 71 148 86 86`

---

## 🚀 Ishga Tushirish va O'rnatish:

### 1. Repozitoriyani klonlash:
```bash
git clone https://github.com/AbdulkhaevHasanboy/idp_ielts_bot.git
cd idp_ielts_bot
```

### 2. Muhitni sozlash:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Ishga tushirish:
```bash
python main.py
```
yoki:
```bash
./run.sh
```

---

## 🌐 24/7 Hosting va Deploy (Railway / Render / Docker / VPS):

- **Railway / Render:** GitHub repo ulanganda [`Procfile`](Procfile) yoki [`Dockerfile`](Dockerfile) orqali 1 bosishda deploy bo'ladi.
- **Linux VPS (systemd):** [`idp-bot.service`](idp-bot.service) faylini `/etc/systemd/system/` ga joylab `systemctl enable --now idp-bot` qiling.

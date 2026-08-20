"""
Comprehensive Gemini AI Service for IDP IELTS Bot.
Supports Gemini 3.1 Flash Live Preview & Gemini multimodal generation for chat,
live background search, images, handwritten essays, and audio voice examination.
"""
import logging
import io
import asyncio
from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL, SUPPORT_USERNAME, SUPPORT_PHONE
from services.search_service import search_web_async

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = f"""You are 'IDP IELTS AI', an elite, concise, and highly helpful AI assistant for IDP IELTS in Uzbekistan (Edu-Action).

CRITICAL COMMUNICATION RULES:
1. NEVER dump unsolicited long boilerplate lists, generic FAQ dumps, or unrelated test center information.
2. Be direct, natural, concise, and focused strictly on the user's specific request or image.
3. Language: Respond in the language of the user (Uzbek by default, Russian, or English).
4. If a user asks for direct human support, manager contact, or Telegram support, provide: Telegram: {SUPPORT_USERNAME} (@idp555) and Call Centre: {SUPPORT_PHONE}.
5. If a question requires live factual verification (dates, university acceptance, recent news), silently search in background and integrate the answer without mentioning you searched.
"""

def get_genai_client():
    api_key = GEMINI_API_KEY
    if not api_key:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

async def generate_ai_chat_response(user_text: str, user_name: str = "Candidate", lang: str = "uz") -> str:
    """
    Generates natural, concise AI response using Gemini 3.1 Flash Live / Gemini model.
    Searches in background only if real-time facts are needed.
    """
    client = get_genai_client()
    if not client:
        return "Assalomu alaykum! IDP IELTS bo'yicha qanday savolingiz bor? Qo'llab-quvvatlash: @idp555" if lang=="uz" else "Здравствуйте! Чем могу помочь по IDP IELTS? Поддержка: @idp555"

    lower = user_text.lower()
    needs_search = any(k in lower for k in [
        "qachon", "sana", "dates", "2026", "2025", "yangi", "latest", "yangilik",
        "universitet", "university", "tan oladimi", "accept", "qaysi davlat"
    ])

    search_context = ""
    if needs_search:
        try:
            search_query = f"IDP IELTS Uzbekistan {user_text}"
            results = await search_web_async(search_query, max_results=3, lang=lang)
            if results:
                snippets = [f"- {r['title']}: {r['snippet']}" for r in results]
                search_context = "\n\nReal-time Web Search Context:\n" + "\n".join(snippets)
        except Exception as e:
            logger.error(f"Silent search error: {e}")

    prompt = f"""User name: {user_name}
User language: {lang}
User message: {user_text}
{search_context}

Provide a concise, helpful, and natural response directly answering the user in {lang}. Do not dump unprompted generic lists. Support member username: {SUPPORT_USERNAME}."""

    # Try Gemini Live API first if model is live preview, otherwise fallback to generate_content
    if "live" in GEMINI_MODEL:
        try:
            async with client.aio.live.connect(
                model=GEMINI_MODEL,
                config=types.LiveConnectConfig(
                    system_instruction=types.Content(parts=[types.Part.from_text(text=SYSTEM_PROMPT)])
                )
            ) as session:
                await session.send_realtime_input(text=prompt)
                full_text = ""
                async for response in session.receive():
                    server_content = response.server_content
                    if server_content and server_content.model_turn:
                        for part in server_content.model_turn.parts:
                            if part.text:
                                full_text += part.text
                    if server_content and server_content.turn_complete:
                        break
                if full_text.strip():
                    return full_text.strip()
        except Exception as e:
            logger.warning(f"Live API chat error ({GEMINI_MODEL}): {e}. Trying generate_content fallback...")

    # Fallback to generate_content with standard models
    def _call_gemini_fallback():
        models_to_try = ["gemini-2.5-flash", "gemini-3.5-flash"]
        for m in models_to_try:
            try:
                response = client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.7,
                    )
                )
                return response.text.strip()
            except Exception as ex:
                logger.error(f"Model {m} error: {ex}")
        return None

    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, _call_gemini_fallback)
    if res:
        return res

    if lang == "uz":
        return f"Assalomu alaykum! Savolingiz bo'yicha yordam berishdan mamnunman. Qo'llab-quvvatlash xodimimiz: {SUPPORT_USERNAME}"
    elif lang == "ru":
        return f"Здравствуйте! Рад помочь вам. Поддержка в Telegram: {SUPPORT_USERNAME}"
    else:
        return f"Hello! How can I assist you? Telegram Support: {SUPPORT_USERNAME}"

async def analyze_image_with_ai(image_bytes: bytes, caption: str = "", lang: str = "uz") -> str:
    """
    Multimodal analysis of images using Gemini 3.1 Flash Live Preview / Gemini Vision.
    """
    client = get_genai_client()
    if not client:
        return "⚠️ API kalit sozlanmagan."

    instruction = f"""Analyze the provided image in detail.
Language for response: {lang}

IMPORTANT RULES:
1. First, clearly state WHAT the image is (e.g. "Ushbu rasmda...").
2. Then, state WHAT should be done with it:

A. If it is UNRELATED to IELTS (e.g. a barcode, object, random photo, invoice, meme):
   - State exactly what it depicts (e.g. "Ushbu rasmda mahsulot shtrix-kodi (barcode) tasvirlangan.").
   - Explain that it is not an IELTS test material.
   - Explain what they can do with the bot instead: if they want to check their IELTS Writing essay, speaking task, reading/listening question, or TRF certificate, they can send that photo and get a complete band score evaluation.
   - CRITICAL: DO NOT dump generic bullet points or test center lists! Keep it short (2-4 sentences).

B. If it is an IELTS Writing Essay (handwritten or typed):
   - Evaluate against the 4 official criteria: Task Achievement (0-9), Coherence & Cohesion (0-9), Lexical Resource (0-9), Grammatical Range & Accuracy (0-9).
   - Estimated Overall Band Score.
   - Exact grammar/vocabulary mistakes with Band 9 corrections.
   - Actionable tips to improve.

C. If it is an IELTS Reading / Listening / Writing Task question or Graph/Chart:
   - Identify the task and provide the step-by-step solution / model answer.

D. If it is an IELTS TRF / Certificate / Score Report:
   - Read the scores, explain CEFR level and university admission requirements.

User caption: {caption}
"""

    # Try Live API first if model is live preview
    if "live" in GEMINI_MODEL:
        try:
            async with client.aio.live.connect(
                model=GEMINI_MODEL,
                config=types.LiveConnectConfig(
                    system_instruction=types.Content(parts=[types.Part.from_text(text=SYSTEM_PROMPT)])
                )
            ) as session:
                await session.send_realtime_input(
                    media_chunks=[types.Blob(data=image_bytes, mime_type="image/jpeg")],
                    text=instruction
                )
                full_text = ""
                async for response in session.receive():
                    server_content = response.server_content
                    if server_content and server_content.model_turn:
                        for part in server_content.model_turn.parts:
                            if part.text:
                                full_text += part.text
                    if server_content and server_content.turn_complete:
                        break
                if full_text.strip():
                    return full_text.strip()
        except Exception as e:
            logger.warning(f"Live API image error ({GEMINI_MODEL}): {e}. Trying generate_content fallback...")

    # Fallback to standard multimodal generate_content
    def _call_gemini_vision_fallback():
        models_to_try = ["gemini-2.5-flash", "gemini-3.5-flash"]
        for m in models_to_try:
            try:
                response = client.models.generate_content(
                    model=m,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                        instruction
                    ],
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.3,
                    )
                )
                return response.text.strip()
            except Exception as ex:
                logger.error(f"Vision model {m} error: {ex}")
        return None

    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, _call_gemini_vision_fallback)
    if res:
        return res

    return "⚠️ Rasmni tahlil qilishda xatolik yuz berdi. Iltimos, qayta yuboring." if lang=="uz" else "⚠️ Error analyzing image."

async def analyze_audio_with_ai(audio_bytes: bytes, mime_type: str = "audio/ogg", lang: str = "uz") -> str:
    """
    Analyzes speaking practice audio recordings using Gemini Live / Gemini Audio.
    """
    client = get_genai_client()
    if not client:
        return "⚠️ API kalit sozlanmagan."

    instruction = f"""You are a certified IELTS Speaking Examiner.
Listen to this candidate's speaking audio recording.
Respond in {lang}.

Structure:
1. 📝 *Xulosa / Matn:* Candidate nima haqida gapirdi.
2. 🎯 *IELTS Mezonlari Baholashi:*
   - *Fluency & Coherence:* (Ravonlik va fikrlar bog'liqligi)
   - *Lexical Resource:* (So'z boyligi va iboralar)
   - *Grammar:* (Grammatik xilma-xillik va aniqlik)
   - *Pronunciation:* (Talaffuz va urg'u)
3. ⭐ *Taxminiy Speaking Band:* (masalan: Band 6.5)
4. 💡 *Band 8+ ga chiqish uchun 2-3 ta aniq maslahat*.
"""

    if "live" in GEMINI_MODEL:
        try:
            async with client.aio.live.connect(
                model=GEMINI_MODEL,
                config=types.LiveConnectConfig(
                    system_instruction=types.Content(parts=[types.Part.from_text(text=SYSTEM_PROMPT)])
                )
            ) as session:
                await session.send_realtime_input(
                    media_chunks=[types.Blob(data=audio_bytes, mime_type=mime_type)],
                    text=instruction
                )
                full_text = ""
                async for response in session.receive():
                    server_content = response.server_content
                    if server_content and server_content.model_turn:
                        for part in server_content.model_turn.parts:
                            if part.text:
                                full_text += part.text
                    if server_content and server_content.turn_complete:
                        break
                if full_text.strip():
                    return full_text.strip()
        except Exception as e:
            logger.warning(f"Live API audio error ({GEMINI_MODEL}): {e}. Trying generate_content fallback...")

    def _call_gemini_audio_fallback():
        models_to_try = ["gemini-2.5-flash", "gemini-3.5-flash"]
        for m in models_to_try:
            try:
                response = client.models.generate_content(
                    model=m,
                    contents=[
                        types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                        instruction
                    ],
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.3,
                    )
                )
                return response.text.strip()
            except Exception as ex:
                logger.error(f"Audio model {m} error: {ex}")
        return None

    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, _call_gemini_audio_fallback)
    if res:
        return res

    return "⚠️ Ovozli xabarni tahlil qilishda xatolik yuz berdi. Iltimos, qaytadan yozib yuboring." if lang=="uz" else "⚠️ Error analyzing audio."

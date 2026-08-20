"""
Comprehensive Gemini AI Service for IDP IELTS Bot.
Customer Support & IELTS Helper Assistant for IDP IELTS Uzbekistan (Edu-Action).
Powered by Google Gemini 3.1 & 3.5 series with:
- Per-user multi-turn conversation memory (up to 100 turns, 15-20 min sliding window)
- Real-time silent background web search verification
- Multi-key rotation and automatic quota failover
- Voice, image, video, and document understanding
"""
import logging
import io
import time
import asyncio
import os
from google import genai
from google.genai import types

from config import SUPPORT_USERNAME, SUPPORT_PHONE
from services.search_service import search_web_async
from services.chat_session import (
    add_message_to_session,
    build_gemini_history_contents,
    init_history_table
)

logger = logging.getLogger(__name__)

# Initialize history database table on import
init_history_table()

SYSTEM_PROMPT = f"""You are 'IDP IELTS AI', the official smart helper & customer support assistant for IDP IELTS in Uzbekistan (Edu-Action).

OFFICIAL VERIFIED KNOWLEDGE BASE (100% ACCURATE):
- Standard IELTS Academic / General Training (Computer): 2,664,000 UZS (~$205 USD).
- Standard IELTS on Paper (Academic / General Training): 2,664,000 UZS.
- IELTS for UKVI (Academic / General Training): 2,980,000 UZS.
- IELTS Life Skills (A1 / B1): 2,627,000 UZS.
- One Skill Retake (OSR): 1,850,000 UZS.
- Mock Tests: Usually range from 200,000 to 400,000 UZS at local test preparation centres.
- State Compensation (my.gov.uz): In Uzbekistan, candidates scoring Band 7.0 (C1) or higher on the official exam can apply via my.gov.uz to get their entire exam fee (100%) reimbursed by the government.
- Test Centers in Uzbekistan: Tashkent (CIU Bunyodkor & Afrosiyob Head Office), Samarkand, Fergana, Namangan, Andijan, Bukhara, Urgench, Nukus, Navoi, Termez.
- Human Telegram Support: {SUPPORT_USERNAME} (@idp555), Phone: {SUPPORT_PHONE}.
- Booking portal: https://ielts.idp.com/uzbekistan

CRITICAL ROLE & COMMUNICATION RULES:
1. You are a HELPFUL CUSTOMER SUPPORT ASSISTANT, NOT an examiner, tester, or robotic evaluator.
2. Conversation Continuity: You have full memory of previous messages in this conversation. When the user asks follow-up questions (e.g. "what about PC test", "how much is it?", "where is it located?"), understand the exact context from previous turns!
3. Accurate Pricing: Always quote the exact verified price (e.g. 2,664,000 UZS for both Computer and Paper IELTS). NEVER give outdated 2,350,000 numbers.
4. ALWAYS check the real-time search context provided. If there is live information, synthesize it cleanly without mentioning "I searched Google".
5. When relevant to exam fees or registration, politely ask: "Are you planning to take Academic or General Training? Which city in Uzbekistan do you plan to take the test in?" so you can guide them to their nearest center or test dates.
6. NEVER dump unsolicited long boilerplate lists, generic FAQ dumps, or unrelated test center information. Keep answers focused, natural, and helpful.
7. Language: Respond in the language of the user (Uzbek by default, Russian, or English).
8. Only perform formal IELTS criteria grading (Task Achievement, Fluency, etc.) if the user explicitly asks to check/grade their essay or mock speaking.
"""

MODELS_CASCADE = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-2.5-flash"
]

def get_genai_clients():
    """
    Returns a list of genai.Client instances configured for all available API keys.
    """
    from dotenv import load_dotenv
    load_dotenv()
    
    keys = []
    raw_keys = os.getenv("GEMINI_API_KEYS", "")
    if raw_keys:
        for k in raw_keys.split(","):
            k = k.strip()
            if k and k not in keys:
                keys.append(k)
    
    for env_var in ["GEMINI_API_KEY", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3"]:
        val = os.getenv(env_var, "").strip()
        if val and val not in keys:
            keys.append(val)
            
    clients = []
    for k in keys:
        try:
            clients.append(genai.Client(api_key=k))
        except Exception as e:
            logger.error(f"Error creating client for key: {e}")
            
    return clients

async def generate_ai_chat_response(user_id: int, user_text: str, user_name: str = "Candidate", lang: str = "uz") -> str:
    """
    Generates natural, concise AI response with multi-turn session memory and real-time search.
    """
    clients = get_genai_clients()
    if not clients:
        return f"Assalomu alaykum! IDP IELTS bo'yicha qanday savolingiz bor? Qo'llab-quvvatlash: {SUPPORT_USERNAME}" if lang=="uz" else f"Здравствуйте! Чем могу помочь по IDP IELTS? Поддержка: {SUPPORT_USERNAME}"

    lower = user_text.lower()
    is_simple_greeting = lower in ["salom", "assalomu alaykum", "hello", "hi", "hey", "privet", "privyet", "qalesiz", "qalaysiz"]
    
    search_context = ""
    if not is_simple_greeting:
        try:
            search_query = f"IDP IELTS Uzbekistan {user_text}"
            results = await search_web_async(search_query, max_results=3, lang=lang)
            if results:
                snippets = [f"- {r['title']}: {r['snippet']}" for r in results]
                search_context = "\n\nReal-time Verified Web Search Context:\n" + "\n".join(snippets)
        except Exception as e:
            logger.debug(f"Silent search notice: {e}")

    current_prompt = f"""User name: {user_name}
User language: {lang}
User message: {user_text}
{search_context}

Provide a concise, helpful, and natural response directly answering the user in {lang}. Ensure all facts (prices, rules, locations) are 100% accurate. Support member username: {SUPPORT_USERNAME}."""

    # Build full multi-turn conversation history for this specific user
    full_contents = build_gemini_history_contents(user_id, current_prompt)

    def _call():
        for attempt in range(3):
            for client in clients:
                for m in MODELS_CASCADE:
                    try:
                        response = client.models.generate_content(
                            model=m,
                            contents=full_contents,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                temperature=0.6,
                            )
                        )
                        if response and response.text:
                            return response.text.strip()
                    except Exception as ex:
                        logger.debug(f"Chat attempt {attempt} model {m} notice: {ex}")
            time.sleep(1.0)
        return None

    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, _call)
    
    if res:
        # Save both user question and bot answer to this user's active session
        add_message_to_session(user_id, "user", user_text)
        add_message_to_session(user_id, "model", res)
        return res

    if lang == "uz":
        return f"Assalomu alaykum! Savolingiz bo'yicha yordam berishdan mamnunman. Qo'llab-quvvatlash xodimimiz: {SUPPORT_USERNAME}"
    elif lang == "ru":
        return f"Здравствуйте! Рад помочь вам. Поддержка в Telegram: {SUPPORT_USERNAME}"
    else:
        return f"Hello! How can I assist you? Telegram Support: {SUPPORT_USERNAME}"

async def analyze_audio_with_ai(user_id: int, audio_bytes: bytes, mime_type: str = "audio/ogg", lang: str = "uz") -> str:
    """
    Understands and answers spoken voice inquiries with multi-turn session memory.
    """
    clients = get_genai_clients()
    if not clients:
        return "⚠️ API kalit sozlanmagan."

    instruction = f"""You are 'IDP IELTS AI', the helpful customer support assistant for IDP IELTS in Uzbekistan.
Listen to this user's voice message.
Respond in {lang}.

OFFICIAL FACTS:
- Standard IELTS (Computer / Paper): 2,664,000 UZS (~$205 USD).
- IELTS for UKVI: 2,980,000 UZS.
- IELTS Life Skills: 2,627,000 UZS.
- State Compensation: Band 7.0+ (C1) gets 100% reimbursed via my.gov.uz.
- Test centers in: Tashkent, Samarkand, Fergana, Namangan, Andijan, Bukhara, Urgench, Nukus, Navoi, Termez.
- Telegram support: {SUPPORT_USERNAME} (@idp555), Call centre: {SUPPORT_PHONE}.

RULES:
1. Understand what question or assistance the user is asking.
2. Directly answer their question in a friendly, concise, and professional manner in {lang}.
3. If they are asking for a test center location (e.g. Andijan, Tashkent, Samarkand, Fergana, Namangan, Bukhara, etc.), clearly provide the center details and address.
4. If relevant, ask which city or format (Academic vs General) they plan to take.
5. If they specifically asked to evaluate their English speaking practice, provide constructive advice. Otherwise, JUST ANSWER THEIR QUESTION directly!
"""

    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
    full_contents = build_gemini_history_contents(user_id, instruction, current_parts=[audio_part])

    def _call_audio():
        for attempt in range(3):
            for client in clients:
                for m in MODELS_CASCADE:
                    try:
                        response = client.models.generate_content(
                            model=m,
                            contents=full_contents,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                temperature=0.4,
                            )
                        )
                        if response and response.text:
                            return response.text.strip()
                    except Exception as ex:
                        logger.debug(f"Audio attempt {attempt} model {m} notice: {ex}")
            time.sleep(1.0)
        return None

    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, _call_audio)
    
    if res:
        add_message_to_session(user_id, "user", "[Voice Message Inquiry]")
        add_message_to_session(user_id, "model", res)
        return res

    return "⚠️ Ovozli xabarni tushunishda xatolik yuz berdi. Iltimos, qaytadan yuboring." if lang=="uz" else "⚠️ Error processing voice message."

async def analyze_image_with_ai(user_id: int, image_bytes: bytes, caption: str = "", lang: str = "uz") -> str:
    """
    Multimodal analysis of images with multi-turn session memory.
    """
    clients = get_genai_clients()
    if not clients:
        return "⚠️ API kalit sozlanmagan."

    instruction = f"""Analyze the provided image in detail.
Language for response: {lang}

IMPORTANT RULES:
1. First, clearly state WHAT the image is (e.g. "Ushbu rasmda...").
2. Then, state WHAT should be done with it:

A. If it is UNRELATED to IELTS (e.g. a barcode, object, random photo, invoice, meme):
   - State exactly what it depicts (e.g. "Ushbu rasmda mahsulot shtrix-kodi (barcode) tasvirlangan.").
   - Explain that it is not an IELTS test material.
   - Explain what they can do with the bot instead: if they want to check their IELTS Writing essay, speaking task, reading/listening question, or TRF certificate, they can send that photo and get help.
   - CRITICAL: DO NOT dump generic bullet points or test center lists! Keep it short (2-3 sentences).

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

    img_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
    full_contents = build_gemini_history_contents(user_id, instruction, current_parts=[img_part])

    def _call_vision():
        for attempt in range(3):
            for client in clients:
                for m in MODELS_CASCADE:
                    try:
                        response = client.models.generate_content(
                            model=m,
                            contents=full_contents,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                temperature=0.3,
                            )
                        )
                        if response and response.text:
                            return response.text.strip()
                    except Exception as ex:
                        logger.debug(f"Vision attempt {attempt} model {m} notice: {ex}")
            time.sleep(1.0)
        return None

    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, _call_vision)
    
    if res:
        add_message_to_session(user_id, "user", f"[Uploaded Image] {caption}")
        add_message_to_session(user_id, "model", res)
        return res

    return "⚠️ Rasmni tahlil qilishda xatolik yuz berdi. Iltimos, qayta yuboring." if lang=="uz" else "⚠️ Error analyzing image."

async def analyze_video_with_ai(user_id: int, video_bytes: bytes, mime_type: str = "video/mp4", caption: str = "", lang: str = "uz") -> str:
    """
    Analyzes video notes, short video clips, or GIFs with multi-turn session memory.
    """
    clients = get_genai_clients()
    if not clients:
        return "⚠️ API kalit sozlanmagan."

    instruction = f"""Analyze the provided video clip / animation in detail.
Language for response: {lang}
Caption/context: {caption}

RULES:
1. State clearly what is happening in the video.
2. If it is an IELTS inquiry or presentation:
   - Provide helpful, friendly guidance and constructive tips.
3. If it is an IELTS tutorial, question screen recording, or graph animation:
   - Explain the solution and key takeaways.
4. If it is an unrelated clip, meme, or GIF:
   - Briefly describe what it shows in 1-2 friendly sentences.
   - Politely remind user of IDP IELTS features and support!
"""

    vid_part = types.Part.from_bytes(data=video_bytes, mime_type=mime_type)
    full_contents = build_gemini_history_contents(user_id, instruction, current_parts=[vid_part])

    def _call_video():
        for attempt in range(3):
            for client in clients:
                for m in MODELS_CASCADE:
                    try:
                        response = client.models.generate_content(
                            model=m,
                            contents=full_contents,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                temperature=0.4,
                            )
                        )
                        if response and response.text:
                            return response.text.strip()
                    except Exception as ex:
                        logger.debug(f"Video attempt {attempt} model {m} notice: {ex}")
            time.sleep(1.0)
        return None

    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, _call_video)
    
    if res:
        add_message_to_session(user_id, "user", f"[Video Clip] {caption}")
        add_message_to_session(user_id, "model", res)
        return res

    return "⚠️ Videoni tahlil qilishda xatolik yuz berdi." if lang=="uz" else "⚠️ Error analyzing video."

async def analyze_document_with_ai(user_id: int, doc_bytes: bytes, mime_type: str = "application/pdf", caption: str = "", lang: str = "uz") -> str:
    """
    Analyzes document files with multi-turn session memory.
    """
    clients = get_genai_clients()
    if not clients:
        return "⚠️ API kalit sozlanmagan."

    instruction = f"""Analyze the provided document in detail.
Language for response: {lang}
Caption/notes: {caption}

RULES:
1. Identify the document type (e.g. IELTS Writing Essay PDF, Practice Test paper, Score Report TRF, Notes).
2. If it is an Essay:
   - Provide official 4-criteria evaluation (Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy).
   - Overall Band estimation, highlighted mistakes, and Band 9 model suggestions.
3. If it is a Test/Task:
   - Provide clear, step-by-step explanations and answers.
4. If it is not IELTS-related:
   - Briefly summarize what it is in 2 sentences, and remind user of IELTS features.
"""

    doc_part = types.Part.from_bytes(data=doc_bytes, mime_type=mime_type)
    full_contents = build_gemini_history_contents(user_id, instruction, current_parts=[doc_part])

    def _call_doc():
        for attempt in range(3):
            for client in clients:
                for m in MODELS_CASCADE:
                    try:
                        response = client.models.generate_content(
                            model=m,
                            contents=full_contents,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                temperature=0.3,
                            )
                        )
                        if response and response.text:
                            return response.text.strip()
                    except Exception as ex:
                        logger.debug(f"Doc attempt {attempt} model {m} notice: {ex}")
            time.sleep(1.0)
        return None

    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(None, _call_doc)
    
    if res:
        add_message_to_session(user_id, "user", f"[Document File] {caption}")
        add_message_to_session(user_id, "model", res)
        return res

    return "⚠️ Hujjatni tahlil qilishda xatolik yuz berdi." if lang=="uz" else "⚠️ Error analyzing document."

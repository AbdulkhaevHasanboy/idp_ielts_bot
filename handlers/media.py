"""
Media handlers for processing photos, handwritten essays, test tasks, TRFs, and voice recordings using AI.
"""
import io
import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.user_state import get_user_language
from services.ai_service import analyze_image_with_ai, analyze_audio_with_ai
from locales import t

logger = logging.getLogger(__name__)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    caption = update.message.caption or ""

    # Get the highest resolution photo
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes_io = io.BytesIO()
    await photo_file.download_to_memory(photo_bytes_io)
    image_bytes = photo_bytes_io.getvalue()

    status_msg = await update.message.reply_text(
        t("ai_analyzing_image", lang),
        reply_to_message_id=update.message.message_id,
        parse_mode="Markdown"
    )

    analysis_result = await analyze_image_with_ai(image_bytes, caption=caption, lang=lang)

    # Edit status message or reply
    try:
        await status_msg.edit_text(analysis_result, parse_mode="Markdown")
    except Exception:
        # Fallback if markdown parsing has special characters from handwriting
        await status_msg.edit_text(analysis_result)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)

    voice_file = await update.message.voice.get_file()
    voice_bytes_io = io.BytesIO()
    await voice_file.download_to_memory(voice_bytes_io)
    audio_bytes = voice_bytes_io.getvalue()

    status_msg = await update.message.reply_text(
        t("ai_analyzing_audio", lang),
        reply_to_message_id=update.message.message_id,
        parse_mode="Markdown"
    )

    audio_result = await analyze_audio_with_ai(audio_bytes, mime_type="audio/ogg", lang=lang)

    try:
        await status_msg.edit_text(audio_result, parse_mode="Markdown")
    except Exception:
        await status_msg.edit_text(audio_result)

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)

    audio_file = await update.message.audio.get_file()
    audio_bytes_io = io.BytesIO()
    await audio_file.download_to_memory(audio_bytes_io)
    audio_bytes = audio_bytes_io.getvalue()

    status_msg = await update.message.reply_text(
        t("ai_analyzing_audio", lang),
        reply_to_message_id=update.message.message_id,
        parse_mode="Markdown"
    )

    audio_result = await analyze_audio_with_ai(audio_bytes, mime_type=update.message.audio.mime_type or "audio/mp3", lang=lang)

    try:
        await status_msg.edit_text(audio_result, parse_mode="Markdown")
    except Exception:
        await status_msg.edit_text(audio_result)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_user_language(user.id)
    doc = update.message.document
    
    if doc.mime_type and ("image" in doc.mime_type or "pdf" in doc.mime_type):
        doc_file = await doc.get_file()
        doc_bytes_io = io.BytesIO()
        await doc_file.download_to_memory(doc_bytes_io)
        doc_bytes = doc_bytes_io.getvalue()

        status_msg = await update.message.reply_text(
            t("ai_analyzing_image", lang),
            reply_to_message_id=update.message.message_id,
            parse_mode="Markdown"
        )

        analysis_result = await analyze_image_with_ai(doc_bytes, caption=update.message.caption or "", lang=lang)
        try:
            await status_msg.edit_text(analysis_result, parse_mode="Markdown")
        except Exception:
            await status_msg.edit_text(analysis_result)

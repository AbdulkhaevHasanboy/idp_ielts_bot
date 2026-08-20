"""
Media handlers for processing photos, handwritten essays, test tasks, TRFs,
voice recordings, video notes (krujochek), GIFs, and PDF documents using AI.
"""
import io
import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.user_state import get_user_language
from services.ai_service import (
    analyze_image_with_ai,
    analyze_audio_with_ai,
    analyze_video_with_ai,
    analyze_document_with_ai
)
from locales import t

logger = logging.getLogger(__name__)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles photos of essays, test tasks, charts, TRFs, barcodes, objects."""
    user = update.effective_user
    lang = get_user_language(user.id)
    caption = update.message.caption or ""

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

    try:
        await status_msg.edit_text(analysis_result, parse_mode="Markdown")
    except Exception:
        await status_msg.edit_text(analysis_result)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles IELTS Speaking voice notes."""
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
    """Handles audio files (MP3, WAV, M4A)."""
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

    mime_type = update.message.audio.mime_type or "audio/mp3"
    audio_result = await analyze_audio_with_ai(audio_bytes, mime_type=mime_type, lang=lang)

    try:
        await status_msg.edit_text(audio_result, parse_mode="Markdown")
    except Exception:
        await status_msg.edit_text(audio_result)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles video files (MP4, MKV, AVI) up to 20MB."""
    user = update.effective_user
    lang = get_user_language(user.id)
    video = update.message.video
    caption = update.message.caption or ""

    if video.file_size and video.file_size > 20 * 1024 * 1024:
        await update.message.reply_text(
            "⚠️ Video hajmi 20MB dan oshmasligi kerak." if lang=="uz" else "⚠️ Video size should be under 20MB.",
            reply_to_message_id=update.message.message_id
        )
        return

    status_msg = await update.message.reply_text(
        "🎬 *AI videoni tahlil qilmoqda...*" if lang=="uz" else "🎬 *AI is analyzing the video...*",
        reply_to_message_id=update.message.message_id,
        parse_mode="Markdown"
    )

    video_file = await video.get_file()
    video_bytes_io = io.BytesIO()
    await video_file.download_to_memory(video_bytes_io)
    video_bytes = video_bytes_io.getvalue()

    mime_type = video.mime_type or "video/mp4"
    result = await analyze_video_with_ai(video_bytes, mime_type=mime_type, caption=caption, lang=lang)

    try:
        await status_msg.edit_text(result, parse_mode="Markdown")
    except Exception:
        await status_msg.edit_text(result)

async def handle_video_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles round video notes (krujochek) for Speaking presentations."""
    user = update.effective_user
    lang = get_user_language(user.id)
    vn = update.message.video_note

    status_msg = await update.message.reply_text(
        "🎥 *AI video xabarni (Speaking) tahlil qilmoqda...*" if lang=="uz" else "🎥 *AI is analyzing your video note...*",
        reply_to_message_id=update.message.message_id,
        parse_mode="Markdown"
    )

    vn_file = await vn.get_file()
    vn_bytes_io = io.BytesIO()
    await vn_file.download_to_memory(vn_bytes_io)
    vn_bytes = vn_bytes_io.getvalue()

    result = await analyze_video_with_ai(vn_bytes, mime_type="video/mp4", caption="Speaking Video Note", lang=lang)

    try:
        await status_msg.edit_text(result, parse_mode="Markdown")
    except Exception:
        await status_msg.edit_text(result)

async def handle_animation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles GIF animations."""
    user = update.effective_user
    lang = get_user_language(user.id)
    anim = update.message.animation

    status_msg = await update.message.reply_text(
        "🎨 *AI animatsiyani (GIF) ko'rib chiqmoqda...*" if lang=="uz" else "🎨 *AI is analyzing the GIF animation...*",
        reply_to_message_id=update.message.message_id,
        parse_mode="Markdown"
    )

    anim_file = await anim.get_file()
    anim_bytes_io = io.BytesIO()
    await anim_file.download_to_memory(anim_bytes_io)
    anim_bytes = anim_bytes_io.getvalue()

    mime_type = anim.mime_type or "video/mp4"
    result = await analyze_video_with_ai(anim_bytes, mime_type=mime_type, caption=update.message.caption or "GIF", lang=lang)

    try:
        await status_msg.edit_text(result, parse_mode="Markdown")
    except Exception:
        await status_msg.edit_text(result)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles documents (PDFs, images sent as documents, docx, txt)."""
    user = update.effective_user
    lang = get_user_language(user.id)
    doc = update.message.document
    caption = update.message.caption or ""

    if doc.file_size and doc.file_size > 20 * 1024 * 1024:
        await update.message.reply_text(
            "⚠️ Hujjat hajmi 20MB dan oshmasligi kerak." if lang=="uz" else "⚠️ Document size must be under 20MB.",
            reply_to_message_id=update.message.message_id
        )
        return

    status_msg = await update.message.reply_text(
        "📄 *AI hujjatni o'qib tahlil qilmoqda...*" if lang=="uz" else "📄 *AI is analyzing the document...*",
        reply_to_message_id=update.message.message_id,
        parse_mode="Markdown"
    )

    doc_file = await doc.get_file()
    doc_bytes_io = io.BytesIO()
    await doc_file.download_to_memory(doc_bytes_io)
    doc_bytes = doc_bytes_io.getvalue()

    mime_type = doc.mime_type or "application/pdf"
    if "image" in mime_type:
        result = await analyze_image_with_ai(doc_bytes, caption=caption, lang=lang)
    elif "video" in mime_type:
        result = await analyze_video_with_ai(doc_bytes, mime_type=mime_type, caption=caption, lang=lang)
    elif "audio" in mime_type:
        result = await analyze_audio_with_ai(doc_bytes, mime_type=mime_type, lang=lang)
    else:
        result = await analyze_document_with_ai(doc_bytes, mime_type=mime_type, caption=caption, lang=lang)

    try:
        await status_msg.edit_text(result, parse_mode="Markdown")
    except Exception:
        await status_msg.edit_text(result)

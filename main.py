"""
Main entry point for IDP IELTS Uzbekistan AI Telegram Bot.
"""
import logging
from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from config import BOT_TOKEN
from services.user_state import init_db
from handlers.commands import (
    cmd_start,
    cmd_help,
    cmd_centers,
    cmd_quiz,
    cmd_speaking,
    cmd_flashcards,
    cmd_calculator,
    cmd_retake,
    cmd_dates,
    cmd_contact,
    cmd_lang
)
from handlers.callbacks import handle_callback_query
from handlers.messages import handle_text_message
from handlers.media import (
    handle_photo,
    handle_voice,
    handle_audio,
    handle_document
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def post_init(application):
    """Set up dynamic bot commands in the menu."""
    commands = [
        BotCommand("start", "Botni ishga tushirish / Главное меню"),
        BotCommand("quiz", "Kunlik IELTS Mashqi / Ежедневный квиз"),
        BotCommand("speaking", "Speaking Part 2 Trenajyor / Тренажер"),
        BotCommand("flashcards", "Band 9 So'zlar / Карточки слов"),
        BotCommand("centers", "Test markazlari & Lokatsiyalar / Центры"),
        BotCommand("calculator", "Band Kalkulyator / Калькулятор"),
        BotCommand("retake", "One Skill Retake (OSR) haqida"),
        BotCommand("dates", "Imtihon sanalari & Narxlar / Регистрация"),
        BotCommand("contact", "Bog'lanish / Контакты"),
        BotCommand("lang", "Tilni o'zgartirish / Сменить язык"),
        BotCommand("help", "Yordam va qo'llanma / Помощь")
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands set successfully.")

def main():
    # 1. Initialize SQLite Database
    init_db()
    logger.info("Database initialized.")

    # 2. Build Telegram Application
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # 3. Register Command Handlers
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(CommandHandler("centers", cmd_centers))
    application.add_handler(CommandHandler("quiz", cmd_quiz))
    application.add_handler(CommandHandler("speaking", cmd_speaking))
    application.add_handler(CommandHandler("flashcards", cmd_flashcards))
    application.add_handler(CommandHandler("calculator", cmd_calculator))
    application.add_handler(CommandHandler("retake", cmd_retake))
    application.add_handler(CommandHandler("dates", cmd_dates))
    application.add_handler(CommandHandler("contact", cmd_contact))
    application.add_handler(CommandHandler("lang", cmd_lang))

    # 4. Register Callback Query Handlers (Interactive buttons, quizzes, flashcards, maps)
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # 5. Register Multimodal Media Handlers (Photos/Essays, Voice, Documents)
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # 6. Register Message Text Handler (AI Chat, Conversations, Calculations)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # 7. Start Polling
    logger.info("Starting IDP IELTS AI Bot polling...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

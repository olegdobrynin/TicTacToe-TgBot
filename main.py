from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from handlers import register, register_callback, register_name, profile_callback, start, handle_move, change_name, change_name_save, rating
from user_data import REGISTER_NAME
import logging

TOKEN = '7072801703:AAGpCOCKwakHrjqa_1cFpAMebZTEA2trP60'

def main():
    application = Application.builder().token(TOKEN).build()

    # Регистрация команд и обработчиков
    registration_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)]
        },
        fallbacks=[]
    )

    change_name_handler = ConversationHandler(
        entry_points=[CommandHandler('change_name', change_name)],
        states={
            REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_name_save)]
        },
        fallbacks=[]
    )

    application.add_handler(registration_handler)
    application.add_handler(change_name_handler)
    application.add_handler(CommandHandler("rating", rating))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("ЗАРЕГИСТРИРОВАТЬСЯ"), register_callback))
    application.add_handler(MessageHandler(filters.Regex("ПРОФИЛЬ"), profile_callback))
    application.add_handler(MessageHandler(filters.Regex("ИГРАТЬ"), start))
    application.add_handler(CallbackQueryHandler(handle_move))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()

from telegram.ext import Application
from handlers import register_handlers
from config import TOKEN

def main():
    application = Application.builder().token(TOKEN).build()
    register_handlers(application)
    application.run_polling()

if __name__ == '__main__':
    main()

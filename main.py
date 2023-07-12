#Internal imports
from apis.credentials import TOKEN
from commands import start_command, help_command, loora_command, plan_command, menu_command, website_command, hello_audio_command
from MessageHandler import handle_message, handle_voice
from buttons import query_handler
from errors import error

#External imports
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import logging


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('loora', loora_command))
    app.add_handler(CommandHandler('plan', plan_command))
    app.add_handler(CommandHandler('menu', menu_command))
    app.add_handler(CommandHandler('website', website_command))
    app.add_handler(CommandHandler('hello', hello_audio_command))

    #Callback Query Handler
    app.add_handler(CallbackQueryHandler(query_handler))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling()
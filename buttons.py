# External
from telegram import Update
from telegram.ext import ContextTypes

# Buttons
async def query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "monthly plan" or query.data == "yearly plan":
        await query.edit_message_text(text=f"Thank you for choosing the {query.data}. Let's make you an account...")
    elif query.data == "nvm":
        await query.edit_message_text(text=f"Still on the fence? You can start with a one week free trial! Download today and check it out! https://apps.apple.com/US/app/id1552708303?mt=8")
    elif query.data == "loora":
        await query.edit_message_text(text=f"Loora is your personal AI English tutor! Download today: https://apps.apple.com/US/app/id1552708303?mt=8")
    elif query.data == "plans":
        await query.edit_message_text(text=f"Do /plan to learn more!")
    elif query.data == "talk":
        await query.edit_message_text(text=f"Hey there!")
    else: 
        await query.edit_message_text(text=f"Do /menu for options!")
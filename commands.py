from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choices = [
        [InlineKeyboardButton('What is Loora', callback_data="loora"), InlineKeyboardButton('View Plans', callback_data="plans")], 
        [InlineKeyboardButton('Talk to CytrynChatBot', callback_data="talk"), InlineKeyboardButton('Help', callback_data="help")]
        ]
    reply_markup = InlineKeyboardMarkup(choices)
    await update.message.reply_text("Hi! I am the <b>CytrynChatBot!</b> Check out /menu to see what I can do.", reply_markup=reply_markup, parse_mode="HTML")

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choices = [['What is Loora', 'View Plans'], ['Talk to CytrynChatBot', 'Help']]
    reply_markup = ReplyKeyboardMarkup(choices, one_time_keyboard=True)
    await update.message.reply_text("Please select a command:", reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("How can I help you?")

async def loora_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Loora is your personal AI English tutor! Download today: https://apps.apple.com/US/app/id1552708303?mt=8")

async def plan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Monthly Plan", callback_data="monthly plan"),
            InlineKeyboardButton("Yearly Plan", callback_data="yearly plan"),
        ],
        [InlineKeyboardButton("Nevermind", callback_data="nvm")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("What plan would you like:", reply_markup=reply_markup)

async def website_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Visit our website: https://www.loora.ai/")

async def hello_audio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_voice("hello_loora.mp3")
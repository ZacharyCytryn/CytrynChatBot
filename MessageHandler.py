# Internal
from AIResponseHandler import handle_response
from apis.credentials import BOT_USERNAME
from apis.TranscriptionHandler import transcribe_audio_file
from apis.TTSHandler import text_to_mp3

# External
from telegram import Update
from telegram.ext import ContextTypes
from pydub import AudioSegment
import os
from datetime import datetime

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    # Captures time received
    user_text_sent_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Creates folder for users if it did not previously exist
    if not os.path.exists("Users"):
        os.mkdir("Users")
    # Creates folder for user if user did not previously have one
    if not os.path.exists(f"Users/{user_id}"):
        os.mkdir(f"Users/{user_id}")
        os.mkdir(f"Users/{user_id}/ReceivedVoiceNotes")
        os.mkdir(f"Users/{user_id}/SentVoiceNotes")
    # Whether group chat or private chat (so bot acts accordingly. Do not want bot to respond in group unless it is being tagged)
    message_type: str = update.message.chat.type
    # Incoming message
    text: str = update.message.text
    # Debug print statement
    print(f'User ({user_id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    # Debug print statement
    print('Bot: ', response)
    
    bot_text_sent_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Write to messages to text file
    if not os.path.exists(f"Users/{user_id}/{user_id}-chat.txt"):
        with open(f'Users/{user_id}/{user_id}-chat.txt', 'w') as file:
            file.write(f"Chat with User_ID: {user_id}\n\n")
            file.write(f"{user_text_sent_at} User: {text}\n")
            file.write(f"{bot_text_sent_at} Bot: {response}\n")
        file.close()
    else:
        with open(f'Users/{user_id}/{user_id}-chat.txt', 'a') as file:
            file.write(f"{user_text_sent_at} User: {text}\n")
            file.write(f"{bot_text_sent_at} Bot: {response}\n")
        file.close()
    print(f"{user_id}-chat.txt in Users/{user_id} updated.")
    await update.message.reply_text(response)

# Handler for voice messages. Downloads, transcribes, and responds
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    # Captures time received
    user_voice_sent_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # Creates folder for users if it did not previously exist
    if not os.path.exists("Users"):
        os.mkdir("Users")
    # Creates folder for user if user did not previously have one
    if not os.path.exists(f"Users/{user_id}"):
        os.mkdir(f"Users/{user_id}")
        os.mkdir(f"Users/{user_id}/ReceivedVoiceNotes")
        os.mkdir(f"Users/{user_id}/SentVoiceNotes")
    # Download file
    file_name = f'{update.update_id}-voice.ogg'
    new_file = await update.message.voice.get_file()
    await new_file.download_to_drive(file_name)
    print(f'{update.update_id}-voice.mp3 saved successfully in the Users/{user_id}/ReceivedVoiceNotes folder.')

    # Transcribe voice
    audio = AudioSegment.from_ogg(file_name)
    audio_file = audio.export(f"{update.update_id}-voice.mp3", format="mp3")
    transcription = transcribe_audio_file(f'{update.update_id}-voice.mp3')
    os.remove(f'{update.update_id}-voice.ogg')
    os.rename(f'{update.update_id}-voice.mp3', f'Users/{user_id}/ReceivedVoiceNotes/{update.update_id}-voice.mp3')

    # Handle Response: Sends voice message, then text
    print(f'User ({user_id}) in {update.message.chat.type} sent a voice note: "{transcription}"')
    response: str = handle_response(transcription)
    print('Bot: ', response)

    # Voice response handling
    # File saved as {update.update_id}response.mp3
    text_to_mp3(update, response)
    await update.message.reply_voice(f"{update.update_id}-response.mp3")
    # Captures time sent
    bot_voice_sent_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    os.rename(f"{update.update_id}-response.mp3", f"Users/{user_id}/SentVoiceNotes/{update.update_id}-response.mp3")
    print(f'Generated speech saved to "{update.update_id}-response.mp3" in the Users/{user_id}/SentVoiceNotes folder.')

    # Write to messages to text file
    if not os.path.exists(f"Users/{user_id}/{user_id}-chat.txt"):
        with open(f'Users/{user_id}/{user_id}-chat.txt', 'w') as file:
            file.write(f"Chat with User_ID: {user_id}\n\n")
            file.write(f"{user_voice_sent_at} User: {transcription}\n")
            file.write(f"{bot_voice_sent_at} Bot: {response}\n")
        file.close()
    else:
        with open(f'Users/{user_id}/{user_id}-chat.txt', 'a') as file:
            file.write(f"{user_voice_sent_at} User: {transcription}\n")
            file.write(f"{bot_voice_sent_at} Bot: {response}\n")
        file.close()
    print(f"{user_id}-chat.txt in Users/{user_id} updated.")

    # Text response handling
    await update.message.reply_text(response)
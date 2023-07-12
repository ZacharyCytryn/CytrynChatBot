# External
import google.cloud.texttospeech as tts
from telegram import Update

# Converts text to an MP3 file. Used for sending voice file of response to user
def text_to_mp3(update: Update, text: str):
    voice_name = "en-US-Studio-O"
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    filename = f"{update.message.chat.id}-{update.update_id}-response.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        
# Test
# text_to_mp3("en-US-Studio-O", "What is the temperature in New York?")
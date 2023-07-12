# External
from google.cloud import speech_v1p1beta1 as speech
# from pydub import AudioSegment

def transcribe_audio_file(audio_file):
    client = speech.SpeechClient()

    with open(audio_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=8000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "

    return transcript.strip()

# Test
# num = "551323277voice"
# audio = AudioSegment.from_ogg("TestAudio/551323277voice.ogg")
# audio_file = audio.export(f"{num}.mp3", format="mp3")
# response = transcribe_audio_file(f"{num}.mp3")
# print(response)
import os
import subprocess
import platform
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs

# Get ElevenLabs API Key from environment variable
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Function to play audio file
def play_audio(output_filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Or use 'mpg123'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"[ERROR] Audio playback failed: {e}")

# Fallback: Text to Speech using gTTS
def text_to_speech_with_gtts(input_text, output_filepath):
    print("[INFO] Using gTTS for text-to-speech...")
    try:
        tts = gTTS(text=input_text, lang="en", slow=False)
        tts.save(output_filepath)
        play_audio(output_filepath)
    except Exception as e:
        print(f"[ERROR] gTTS failed: {e}")

# Primary: Text to Speech using ElevenLabs
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    print("[INFO] Attempting text-to-speech with ElevenLabs...")
    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.text_to_speech.convert(
            text=input_text,
            voice_id="ZF6FPAbjXT4488VcRRnw",  # Replace with your desired voice ID
            model_id="eleven_multilingual_v2",
            output_format="mp3_22050_32",
        )
        elevenlabs.save(audio, output_filepath)
        play_audio(output_filepath)
    except Exception as e:
        print(f"[WARNING] ElevenLabs failed: {e}")
        text_to_speech_with_gtts(input_text, output_filepath)

# Example usage
# input_text = "Hello! This is a voice test using ElevenLabs with fallback to gTTS."
# output_file = "output_voice.mp3"
# text_to_speech_with_elevenlabs(input_text, output_file)

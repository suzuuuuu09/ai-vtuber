import requests, os
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf

load_dotenv()

VOICEVOX_API_KEY = os.getenv('VOICEVOX_API_KEY')
VOICEVOX_API_URL = f"https://deprecatedapis.tts.quest/v2/voicevox/audio/"
AUDIO_FILE_PATH = "audio/output.wav"
speaker_id = 1

class VoiceVoxPlayer:
    def __init__(self, api_key: str = VOICEVOX_API_KEY, 
                 api_url: str = VOICEVOX_API_URL, 
                 audio_file_path: str = AUDIO_FILE_PATH):
        self.api_key = api_key
        self.api_url = api_url
        self.audio_file_path = audio_file_path

    def generate_audio(self, text: str):
        params = {
            "key": self.api_key,
            "speaker": speaker_id,
            "pitch": 0,
            "intonationScale": 1,
            "speed": 1,
            "text": text
        }

        response = requests.post(self.api_url, params=params)

        if response.status_code == 200:
            audio_data = response.content

            os.makedirs(os.path.dirname(self.audio_file_path), exist_ok=True)
            with open(self.audio_file_path, "wb") as f:
                f.write(audio_data)
            return self.audio_file_path
        
    def play_audio(self):
        sound_data, samplerate = sf.read(self.audio_file_path)
        sd.play(sound_data, samplerate)
        sd.wait()


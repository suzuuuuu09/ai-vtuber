import requests, os
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf

load_dotenv()

VOICEVOX_API_KEY = os.getenv('VOICEVOX_API_KEY')
VOICEVOX_API_URL = "https://deprecatedapis.tts.quest/v2/voicevox/audio/"
# AUDIO_FILE_PATH = "audio/output.wav"
speaker_id = 10

class VoiceVoxPlayer:
    def __init__(self, api_key: str = VOICEVOX_API_KEY, 
                 api_url: str = VOICEVOX_API_URL):
        self.api_key = api_key
        self.api_url = api_url

    def generate_audio(self, text: str, path: str):
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

            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(audio_data)
            return path
        
    def play_audio(self, path):
        sound_data, samplerate = sf.read(path)
        sd.play(sound_data, samplerate)
        sd.wait()

if __name__ == "__main__":
    player = VoiceVoxPlayer()
    audio_file_path = player.generate_audio("こんにちは！", "audio/output.wav")
    player.play_audio(audio_file_path)
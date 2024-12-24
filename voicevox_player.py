import os
import asyncio
import aiohttp
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv

load_dotenv()

VOICEVOX_API_KEY = os.getenv('VOICEVOX_API_KEY')
VOICEVOX_API_URL = "https://deprecatedapis.tts.quest/v2/voicevox/audio/"
speaker_id = 10

class VoiceVoxPlayer:
    def __init__(self, api_key: str = VOICEVOX_API_KEY, 
                 api_url: str = VOICEVOX_API_URL):
        self.api_key = api_key
        self.api_url = api_url

    async def generate_audio(self, text: str, path: str):
        params = {
            "key": self.api_key,
            "speaker": speaker_id,
            "pitch": 0,
            "intonationScale": 1,
            "speed": 1,
            "text": text
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, params=params) as response:
                if response.status == 200:
                    audio_data = await response.read()

                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "wb") as f:
                        f.write(audio_data)
                    return path
                else:
                    print(f"Failed to generate audio. Status code: {response.status}")
                    return None

    async def play_audio(self, path):
        loop = asyncio.get_event_loop()
        sound_data, samplerate = sf.read(path)
        await loop.run_in_executor(None, lambda: self._sync_play_audio(sound_data, samplerate))

    def _sync_play_audio(self, sound_data, samplerate):
        sd.play(sound_data, samplerate)
        sd.wait()

async def main():
    player = VoiceVoxPlayer()

    # 非同期で音声生成
    tasks = [
        player.generate_audio("こんにちは！", "audio/output.wav"),
        player.generate_audio("おはよう！", "audio/test.wav")
    ]

    audio_paths = await asyncio.gather(*tasks)

    # 生成した音声を順次再生
    for path in audio_paths:
        if path:
            player.play_audio(path)

if __name__ == "__main__":
    asyncio.run(main())

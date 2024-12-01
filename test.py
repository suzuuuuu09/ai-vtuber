from repsponse_chatgpt import ResponseChatGPT
from voicevox_player import VoiceVoxPlayer

response = ResponseChatGPT()
reply = response.send_message("You are a helpful assistant.", "こんにちは。")

player = VoiceVoxPlayer(text=reply)

try:
    audio_file = player.generate_audio()
    player.play_audio()
except Exception as e:
    print(f"Error: {e}")
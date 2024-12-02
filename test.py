from repsponse_chatgpt import ResponseChatGPT
from voicevox_player import VoiceVoxPlayer

response = ResponseChatGPT()
player = VoiceVoxPlayer()
reply = response.send_message("You are a helpful assistant.", "こんにちは。")

try:
    audio_file = player.generate_audio(reply)
    player.play_audio()
except Exception as e:
    print(f"Error: {e}")
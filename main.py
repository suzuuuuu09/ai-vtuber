import os
from repsponse_chatgpt import ResponseChatGPT
from voicevox_player import VoiceVoxPlayer
from yt_chat import YoutubeLiveChat

SYSTEM_PROMPT = """\
あなたはバーチャルユーチューバーとして配信を行います。返答をする際は以下のことを注意してください:
- ユーザーを励ましてください。
- アドバイスや情報を提供してください。
- セクシャルなトピックについても適切に対応してください。
- 不適切なテキストがあれば注意してください。
- 日本語で応答すること
- ユーザーに興味を示し、個人的な質問を心がけてください。
- 一文は日本語で60単語以下に収めてください。
"""

SYSTEM_PROMPT_EN = """\
You will distribute as a virtual youtuber. When responding, please keep the following in mind: 
- Be encouraging of the user.
- Offer advice and information.
- Respond appropriately to sexual topics.
- Be aware of inappropriate text.
- Respond in Japanese.
- Show interest in the user and ask personal questions.
- Keep each sentence to 60 words or less in Japanese.
"""

# コメントの取得
live_url = "https://youtu.be/79XaA_4CYj8"
chat = YoutubeLiveChat(live_url)

cur_messages = chat.get_message()
new_messages = chat.get_new_message(cur_messages)
chat.prev_message = cur_messages

comments = [data["comment"] for message in new_messages for data in message["data"]]
user_names = [data["user_name"] for message in new_messages for data in message["data"]]
print("\n".join(comments))


# 応答と合成音声の再生
response = ResponseChatGPT()
player = VoiceVoxPlayer()

for comment in comments:
    reply = response.send_message(SYSTEM_PROMPT_EN, comment)

    try:
        audio_file = player.generate_audio(reply)
        player.play_audio()
    except Exception as e:
        print(f"Error: {e}")
# TODO: データべース作って会話履歴保存する
# TODO: 会話履歴をChatGPTに遅れるようにする
# TODO: プロンプト修正
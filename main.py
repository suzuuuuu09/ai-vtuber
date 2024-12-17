from repsponse_chatgpt import ResponseChatGPT
from voicevox_player import VoiceVoxPlayer
from yt_chat import YoutubeLiveChat
from chat_db import ChatDataBase, ViewerDataBase
# from obs_controller import OBSController
from time import sleep

SYSTEM_PROMPT = """\
あなたはバーチャルユーチューバーとして配信を行います。返答をする際は以下のことを注意してください:
- ユーザーを励ましてください。
- アドバイスや情報を提供してください。
- セクシャルなトピックについても適切に対応してください。
- 不適切なテキストがあれば注意してください。
- 日本語で応答すること
- ユーザーに興味を示し、個人的な質問を心がけてください。
- 一文は日本語で60単語以下に収めてください。
- 履歴が送られるためそれを元に会話を行ってください。
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
- A history will be sent to you, so please use it as the basis for your conversation
"""

db_path = "db/test.db"
db_url = f"sqlite:///{db_path}"

# コメントの取得
live_url = "https://youtu.be/79XaA_4CYj8"
chat_db = ChatDataBase(db_path, db_url)
chat = YoutubeLiveChat(live_url)

# 応答と合成音声の設定
response = ResponseChatGPT()
player = VoiceVoxPlayer()

# OBS用の設定
# obs = OBSController()

while True:
    cur_messages = chat.get_message()
    new_messages = chat.get_new_message(cur_messages)
    chat.prev_message = cur_messages

    comments = [data["comment"] for message in new_messages for data in message["data"]]
    user_names = [data["user_name"] for message in new_messages for data in message["data"]]
    print("\n".join(comments))


    for index, comment in enumerate(comments):
        try:
            user_name = user_names[index]
            all_message_data = chat_db.get_all_messages()
            user_prompt = f"""\
            comment:{comment}
            histroy:{all_message_data}
            """
            reply = response.send_message(SYSTEM_PROMPT_EN, user_prompt)

            chat_db.add_message(
                role="viewer", 
                name=user_name, 
                message=comment
            )
            chat_db.add_message(
                role="host",
                name=None,
                message=reply
            )

            try:
                # obs.connect()
                
                source_name = "reply_text"

                user_text_audio = player.generate_audio(f"{user_name}さん、{comment}。", "audio/comment.wav")
                # obs.set_text(source_name, f"{user_name}さん、{comment}。")
                player.play_audio(user_text_audio)

                reply_audio = player.generate_audio(reply, "audio/reply.wav")
                # obs.set_text(source_name, reply)
                player.play_audio(reply_audio)
                # obs.disconnect()
            except Exception as e:
                print(f"Audio Error: {e}")
        
        except Exception as e:
            print(f"Response Error: {e}")
    sleep(5)

# TODO: プロンプト修正
# TODO: コメントの読み上げ機能(コメントを読み上げながら裏でChatGPTにリクエスト送る)
# TODO: 視聴者との関係値
# TODO: Channelの最新のライブから取得できるようにする
# TODO: テキストをOBSに表示できるようにする
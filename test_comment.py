from yt_chat import YoutubeLiveChat

video_url = "https://youtu.be/gPjDmXCHvkM"
yt_chat = YoutubeLiveChat(video_url)

cur_messages = yt_chat.get_message()
new_messages = yt_chat.get_new_message(cur_messages)
yt_chat.prev_message = cur_messages
# print(json.dumps(new_messages, indent=2, ensure_ascii=False))

comments = [data["comment"] for message in new_messages for data in message["data"]]
user_names = [data["user_name"] for message in new_messages for data in message["data"]]
print("\n".join(comments))
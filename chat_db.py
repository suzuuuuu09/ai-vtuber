import dataset

class ChatDataBase():
    def __init__(self, db_url):
        self.db = dataset.connect(db_url)
        self.conv_table = self.db["conversation"]

    def add_message(self, role, name, message):
        self.conv_table.insert({
            "role": role,
            "name": name if role == "host" else None,
            "message": message
        })

    def clear_all_messages(self):
        self.conv_table.delete()

    def get_all_messages(self):
        return list(dict(row) for row in self.conv_table.all())

class ViewerDataBase():
    def __init__(self, db_url):
        self.db = dataset.connect(db_url)
        self.viewer_table = self.db["viewer"]

if __name__ == "__main__":
    chat_db = ChatDataBase("sqlite:///db/test.db")

    chat_db.clear_all_messages()
    chat_db.add_message("host", "Bot", "Hello, I'm a chatbot!")
    chat_db.add_message("viewer", "Alice", "Hi, nice to meet you!")

    print(chat_db.get_all_messages())
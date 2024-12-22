import dataset
import os

class ChatDataBase():
    def __init__(self, db_path, db_url):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db = dataset.connect(db_url)
        self.conv_table = self.db["conversation"]
        self.conv_table.delete()

    def add_message(self, role, message, name):
        self.conv_table.insert({
            "role": role,
            "name": name,
            "message": message
        })

    def clear_all_messages(self):
        self.conv_table.delete()

    def get_all_messages(self):
        return list(dict(row) for row in self.conv_table.all())

class ViewerDataBase():
    def __init__(self, db_path, db_url):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db = dataset.connect(db_url)
        self.viewer_table = self.db["viewer"]
        # self.viewer_table.delete()

    def upsert_viewer_info(self, user_id, user_name):
        # self.viewer_table.insert({
        #     "user_id": user_id,
        #     "user_name": user_name
        # })
        existing_user = self.viewer_table.find_one(user_id=user_id)

        if existing_user:
            self.viewer_table.update({
                "user_name": user_name
            }, ["user_id"])
        else:
            self.viewer_table.insert({
                "user_id": user_id,
                "user_name": user_name
            })

    def clear_all_viewer_info(self):
        self.viewer_table.delete()

    def get_all_viewer_info(self):
        return list(dict(row) for row in self.viewer_table.all())

if __name__ == "__main__":
    db_path = "db/test.db"
    db_url = f"sqlite:///{db_path}"
    # chat_db = ChatDataBase(db_path, db_url)

    # chat_db.clear_all_messages()
    # chat_db.add_message("host", "Bot", "Hello, I'm a chatbot!")
    # chat_db.add_message("viewer", "Alice", "Hi, nice to meet you!")

    # print(chat_db.get_all_messages())

    viewer_db = ViewerDataBase(db_path, db_url)

    viewer_db.upsert_viewer_info("user123", "uuuuuuuuuuuuuuuuuuuu")
    viewer_db.upsert_viewer_info("user456", "Bob")

    print(viewer_db.get_all_viewer_info())

    # TODO: viewer_infoのupsert機能の完成
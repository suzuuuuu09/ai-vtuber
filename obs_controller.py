import os
from obswebsocket import obsws, requests
from dotenv import load_dotenv


class OBSController:
    def __init__(self, host="localhost", port=None, password=None):
        load_dotenv()
        self.host = host
        self.port = port or os.getenv("OBS_WEBSOCKET_PORT")
        self.password = password or os.getenv("OBS_WEBSOCKET_PASS")
        self.ws = None

    def connect(self):
        try:
            self.ws = obsws(self.host, self.port, self.password)
            self.ws.connect()
            print("OBS WebSocketに接続しました")
        except Exception as e:
            print(f"接続エラー: {e}")

    def set_text(self, source_name, text):
        if not self.ws:
            print("WebSocketが接続されていません")
            return

        try:
            # 現在の入力設定を取得
            response = self.ws.call(requests.GetInputSettings(source_name))
            current_settings = response.getInputSettings()

            # "text" のみ更新
            current_settings["text"] = text

            # 設定を反映
            self.ws.call(requests.SetInputSettings(
                source_name,
                current_settings  # 取得した設定を更新
            ))
            print(f"テキストを設定しました: {text}")
        except Exception as e:
            print(f"エラー: {e}")

    def disconnect(self):
        if self.ws:
            try:
                self.ws.disconnect()
                print("OBS WebSocket接続を終了しました")
            except Exception as e:
                print(f"切断エラー: {e}")


if __name__ == "__main__":
    obs = OBSController()
    obs.connect()
    obs.set_text("reply_text", "yoro")
    obs.disconnect()

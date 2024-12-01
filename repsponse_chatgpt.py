import requests, os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
CHATGPT_MODEL = "gpt-4o-mini"

class ResponseChatGPT:
    def __init__(self, model = CHATGPT_MODEL, api_key = OPENAI_API_KEY, api_url = OPENAI_API_URL):
        self.model = model
        self.api_key = api_key
        self.api_url = api_url

    def send_message(self, sys_prompt: str, user_prompt: str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "max_tokens": 100,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        response = requests.post(self.api_url, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            reply = response_data["choices"][0]["message"]["content"]
            return reply
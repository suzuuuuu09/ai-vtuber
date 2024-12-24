import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
CHATGPT_MODEL = "gpt-4o-mini"

class ResponseChatGPT:
    def __init__(self, model=CHATGPT_MODEL, api_key=OPENAI_API_KEY, api_url=OPENAI_API_URL):
        self.model = model
        self.api_key = api_key
        self.api_url = api_url

    async def send_message(self, sys_prompt: str, user_prompt: str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=data, headers=headers) as response:
                if response.status == 200:
                    response_data = await response.json()
                    reply = response_data["choices"][0]["message"]["content"]
                    print(f"Host: {reply}")
                    return reply
                else:
                    error_message = await response.text()
                    print(f"Error: {response.status}, Message: {error_message}")
                    raise Exception(f"Request failed with status {response.status}: {error_message}")

if __name__ == "__main__":
    async def main():
        chat = ResponseChatGPT()
        sys_prompt = "Your Human."
        user_prompt_1 = "What is your favorite color?"
        user_prompt_2 = "What is your favorite animal?"

        try:
            responses = await asyncio.gather(
                chat.send_message(sys_prompt, user_prompt_1),
                chat.send_message(sys_prompt, user_prompt_2)
            )

            for i, response in enumerate(responses, start=1):
                print(f"User {i}: {response}")

        except Exception as e:
            print(f"An error occurred: {e}")

    asyncio.run(main())
import requests, os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_API_URL = "https://www.googleapis.com/youtube/v3/"
video_id = ""

# params = {
#     'key': GOOGLE_API_KEY,
#     'part': 'snippet',
#     'videoId': video_id,
#     'order': 'relevance',
#     'textFormat': 'plaintext',
#     'maxResults': 100,
# }

# if next_page_token is not None:
#     params['pageToken'] = next_page_token
# response = requests.get(URL + 'commentThreads', params=params)
# resource = response.json()
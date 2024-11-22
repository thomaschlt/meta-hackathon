from hgooglenews import get_google_news
from hhackernews import search_hackernews_sync
import json

def get_update_news():
    interest = ["NVIDIA", "TESLA", "GOOGLE GEMINI", "META QUEST 4"]
    news_data = []
    for topic in interest:
        google_news = get_google_news(topic)
        hackernews = search_hackernews_sync(topic)
        news_data= news_data+google_news + hackernews
    return json.dumps(news_data)


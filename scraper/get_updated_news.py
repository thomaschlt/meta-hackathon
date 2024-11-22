from scraper.hgooglenews import get_google_news
from scraper.hhackernews import search_hackernews_sync
from scraper.hyoutube import get_youtube_subscription_videos
from scraper.hspotify import get_recent_and_interesting_music
import json

def get_update_news():
    interest = ["NVIDIA", "TESLA", "GOOGLE GEMINI", "META QUEST 4"]
    news_data = []
    for topic in interest:
        google_news = get_google_news(topic)
        hackernews = search_hackernews_sync(topic)
        youtube_feed = get_youtube_subscription_videos()
        spotify_feed = get_recent_and_interesting_music()
        news_data= news_data+google_news + hackernews +youtube_feed+spotify_feed
    return json.dumps({"news_list" : news_data})


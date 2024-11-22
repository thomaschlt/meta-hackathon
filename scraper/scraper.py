import asyncio
from crawl4ai import AsyncWebCrawler

async def scrape_youtube_with_profile_mac():
    """Scrapes video titles and links from YouTube using an existing Chrome profile."""
    chrome_user_data_dir = "/Users/YourUsername/Library/Application Support/Google/Chrome/Default"  # Update with your path

    async with AsyncWebCrawler(
        browser_type="chromium",          # Use Chromium browser
        headless=False,                  # Show browser GUI for debugging
        user_data_dir=chrome_user_data_dir,  # Use your Chrome profile
        verbose=True                     # Enable detailed logging
    ) as crawler:
        result = await crawler.arun(
            url="https://www.youtube.com",
            wait_for="css:#content",     # Wait for the main content to load
            js_code=[                    # Scroll the page to load more videos
                "let totalHeight = 0;",
                "const distance = 100;",
                "const scrollInterval = setInterval(() => {",
                "  window.scrollBy(0, distance);",
                "  totalHeight += distance;",
                "  if (totalHeight >= document.body.scrollHeight) {",
                "    clearInterval(scrollInterval);",
                "  }",
                "}, 200);"
            ],
            delay_before_return_html=3.0,   # Wait for content to render
            css_selector="ytd-rich-item-renderer"  # Select video containers
        )

        if result.success:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(result.html, 'html.parser')
            videos = []
            for video in soup.select("ytd-rich-item-renderer"):
                title = video.select_one("#video-title").text.strip() if video.select_one("#video-title") else "No Title"
                link = "https://www.youtube.com" + video.select_one("#video-title")['href'] if video.select_one("#video-title") else "No Link"
                videos.append({"title": title, "link": link})

            print(f"Extracted {len(videos)} videos:")
            for video in videos:
                print(f"{video['title']} -> {video['link']}")
        else:
            print(f"Failed to scrape YouTube: {result.error_message}")

asyncio.run(scrape_youtube_with_profile_mac())

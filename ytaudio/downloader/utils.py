import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from .models import YouTubeChannel, MediaURL
from django.utils import timezone

def get_channel_id(youtube_url):
    """Extract channelId from YouTube channel page source."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(youtube_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        meta = soup.find("meta", property="og:url")
        if meta and '/channel/' in meta.get("content", ""):
            return meta["content"].split('/channel/')[1].split("?")[0]

        link = soup.find("link", rel="canonical")
        if link and '/channel/' in link.get("href", ""):
            return link["href"].split('/channel/')[1].split("?")[0]

    except Exception as e:
        print("❌ Error extracting channel ID:", e)
    return None

def fetch_and_save_media_urls(youtube_channel):
    """Fetch media URLs and store in MediaURL model."""
    if not youtube_channel.channel_id:
        channel_id = get_channel_id(youtube_channel.url)
        if channel_id:
            youtube_channel.channel_id = channel_id
            youtube_channel.save()
        else:
            return

    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={youtube_channel.channel_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(rss_url, headers=headers)
        root = ET.fromstring(response.content)

        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'media': 'http://search.yahoo.com/mrss/',
            'yt': 'http://www.youtube.com/xml/schemas/2015'
        }

        for entry in root.findall('atom:entry', ns):
            media_content = entry.find('media:group/media:content', ns)
            if media_content is not None:
                url = media_content.attrib.get('url')
                if url and not MediaURL.objects.filter(media_url=url).exists():
                    MediaURL.objects.create(
                        youtube_channel=youtube_channel,
                        media_url=url,
                        created_at=timezone.now()
                    )
                    print(f"✅ New media URL saved: {url}")
    except Exception as e:
        print("❌ Error fetching RSS:", e)

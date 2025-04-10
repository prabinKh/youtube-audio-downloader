import requests
import xml.etree.ElementTree as ET
import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from downloader.models import YouTubeChannel, MediaURL


class Command(BaseCommand):
    help = "Check and update Media URLs for all YouTube channels every 10 seconds."

    def handle(self, *args, **kwargs):
        while True:
            youtube_channels = YouTubeChannel.objects.all()

            for youtube_channel in youtube_channels:
                self.stdout.write(f"Checking updates for YouTube Channel: {youtube_channel.name} ({youtube_channel.channel_id})")
                
                # Create RSS URL
                rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={youtube_channel.channel_id}"
                headers = {"User-Agent": "Mozilla/5.0"}

                try:
                    response = requests.get(rss_url, headers=headers)
                    response.raise_for_status()  
                    root = ET.fromstring(response.content)

                    ns = {
                        'atom': 'http://www.w3.org/2005/Atom',
                        'media': 'http://search.yahoo.com/mrss/',
                        'yt': 'http://www.youtube.com/xml/schemas/2015'
                    }

                    # Fetch all media URLs already stored for the channel
                    existing_urls = set(
                        MediaURL.objects.filter(youtube_channel=youtube_channel)
                        .values_list('media_url', flat=True)
                    )

                    # Loop through all entries in the RSS feed
                    for entry in root.findall('atom:entry', ns):
                        media_content = entry.find('media:group/media:content', ns)
                        if media_content is not None:
                            url = media_content.attrib.get('url')
                            if url and url not in existing_urls:
                                MediaURL.objects.create(
                                    youtube_channel=youtube_channel,
                                    media_url=url,
                                    created_at=timezone.now()
                                )
                                self.stdout.write(f"✅ New media URL added: {url}")
                                existing_urls.add(url)  
                            else:
                                self.stdout.write(f" Media URL already exists: {url}")

                except requests.exceptions.RequestException as e:
                    self.stdout.write(f" Error fetching RSS for {youtube_channel.name}: {e}")
                except Exception as e:
                    self.stdout.write(f"❌ Unexpected error: {e}")

            self.stdout.write("⏳ Waiting for 10 seconds before checking again...")
            time.sleep(100)

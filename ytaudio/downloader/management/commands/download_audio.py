import os
import subprocess
import time
import re
from pathlib import Path
from django.core.files import File  # Import File for FileField
from django.core.management.base import BaseCommand
from django.conf import settings
from downloader.models import MediaURL, DownloadedAudio  # Ensure your app name is correct

class Command(BaseCommand):
    help = "Download audio from YouTube URLs and save the audio file paths."

    def handle(self, *args, **kwargs):
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
        os.makedirs(audio_dir, exist_ok=True)

        while True:
           
            media_urls = MediaURL.objects.exclude(id__in=DownloadedAudio.objects.values('media_url'))

            if media_urls.exists():
                for media in media_urls:
                    url = media.media_url

                    try:
                      
                        filename = url.split("/")[-1]
                        filename = re.sub(r'\?.*$', '', filename) 
                        filename = re.sub(r'[^a-zA-Z0-9_-]', '_', filename)  

                       
                        output_template = os.path.join(audio_dir, f"{filename}.%(ext)s")
                        absolute_audio_path = os.path.join(audio_dir, f"{filename}.mp3")

                      
                        command = [
                            'yt-dlp',
                            '-x', 
                            '--audio-format', 'mp3',
                            '--audio-quality', '0',  
                            '--output', output_template,
                            url
                        ]

                        subprocess.run(command, check=True)

                        if not os.path.exists(absolute_audio_path):
                            raise FileNotFoundError(f"Audio file not found at {absolute_audio_path}")

                        with open(absolute_audio_path, 'rb') as audio_file:
                            downloaded_audio = DownloadedAudio(
                                media_url=media,
                                audio_file=File(audio_file, name=f"{filename}.mp3")
                            )
                            downloaded_audio.save()

                        self.stdout.write(f"✅ Downloaded and saved audio for: {url}")

                    except subprocess.CalledProcessError as e:
                        self.stdout.write(f" yt-dlp failed for {url}: {e}")
                    except FileNotFoundError as e:
                        self.stdout.write(f" File error for {url}: {e}")
                    except Exception as e:
                        self.stdout.write(f" Unexpected error for {url}: {str(e)}")
            else:
                self.stdout.write(" No new media URLs to download.")

            self.stdout.write("⏳ Waiting 10 seconds...")
            time.sleep(10)
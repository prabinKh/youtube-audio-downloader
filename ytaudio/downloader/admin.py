from django.contrib import admin

from .models import YouTubeChannel, MediaURL , DownloadedAudio

admin.site.register(YouTubeChannel) 
admin.site.register(MediaURL) 
admin.site.register(DownloadedAudio)

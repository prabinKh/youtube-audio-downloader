from django.shortcuts import render, redirect
from .models import YouTubeChannel, MediaURL
from .forms import YouTubeChannelForm
from .utils import fetch_and_save_media_urls

def channel_list(request):
    channels = YouTubeChannel.objects.all()
    return render(request, 'downloader/channel_list.html', {'channels': channels})

def add_channel(request):
    if request.method == 'POST':
        form = YouTubeChannelForm(request.POST)
        if form.is_valid():
            channel = form.save()
            fetch_and_save_media_urls(channel)
            return redirect('channel_list') 
    else:
        form = YouTubeChannelForm()
    return render(request, 'downloader/add_channel.html', {'form': form})

def media_list(request, channel_id):
    channel = YouTubeChannel.objects.get(id=channel_id)
    media_urls = channel.media_urls.all()
    return render(request, 'downloader/media_list.html', {
        'channel': channel,
        'media_urls': media_urls
    })

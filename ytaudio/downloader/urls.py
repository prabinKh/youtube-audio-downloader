# yourapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.channel_list, name='channel_list'),  
    path('add/', views.add_channel, name='add_channel'), 
    path('channel/<int:channel_id>/', views.media_list, name='media_list'),  
]

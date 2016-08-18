# mysite/fb_champions/urls.py
from django.conf.urls import include, url
from .views import ChampionsBotView
urlpatterns = [
                 url(r'^0869124024cade4aa12a1211406da868d7617310a15892d6b6/?$', ChampionsBotView.as_view())
]

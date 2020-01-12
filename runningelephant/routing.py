from django.urls import path
from runningelephant.consumers import ProfileConsumer

websocket_urlpatterns = [
    path('ws/profile/', ProfileConsumer),
]

from django.urls import path
from . import consumers  # WebSocket consumer'larını burada kullanacağız

websocket_urlpatterns = [
    path('ws/attendance/', consumers.AttendanceConsumer.as_asgi()),
]

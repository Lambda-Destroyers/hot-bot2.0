from rest_framework import generics
from .serializer import HotBotSerializer
from .models import HotBot


class HotBotList(generics.ListCreateAPIView):
    queryset = HotBot.objects.all()
    serializer_class = HotBotSerializer


class HotBotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotBot.objects.all()
    serializer_class = HotBotSerializer

# Create your views here.


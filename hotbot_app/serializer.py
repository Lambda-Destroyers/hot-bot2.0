from rest_framework import serializers
from .models import HotBot

class HotBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotBot
        fields = ('id', 'price', 'currency', 'bot_run_time', 'desired_ROI', 'stop_loss', 'owner')

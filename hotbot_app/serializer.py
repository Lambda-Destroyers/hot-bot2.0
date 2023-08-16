from rest_framework import serializers
from .models import HotBot


class HotBotSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'owner', 'name', 'description', 'updated_at', 'created_at')
        model = HotBot
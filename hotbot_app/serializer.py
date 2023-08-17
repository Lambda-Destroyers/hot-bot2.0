from rest_framework import serializers
from .models import  Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('transaction_id', 'price', 'size', 'product_id', 'side', 'transaction_type', 'created_at','status', )
       


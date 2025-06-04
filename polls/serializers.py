from rest_framework import serializers
from .models import Item  # Supondo que você tenha um modelo chamado 'Item'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'  # Isso serializa todos os campos do modelo 'Item'

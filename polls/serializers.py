from rest_framework import serializers
from .models import Item  # Supondo que você tenha um modelo chamado 'Item'
from django.utils.timezone import localtime

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'  # Isso serializa todos os campos do modelo 'Item'

class MovimentoSerializer(serializers.ModelSerializer):
    data_hora = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'tipo', 'data_hora', 'outros_campos']  # ajuste os campos conforme seu modelo

    def get_data_hora(self, obj):
        return localtime(obj.data_hora).strftime('%Y-%m-%d %H:%M:%S')
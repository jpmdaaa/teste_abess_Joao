from rest_framework import serializers
from .models import Cotacao

class CotacaoSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    
    class Meta:
        model = Cotacao
        fields = ['id', 'moeda', 'valor', 'data']
    
    def get_data(self, obj):
        return obj.data.strftime("%Y-%m-%d")  # Usando o campo 'data' no lugar de 'created_at'

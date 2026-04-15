from rest_framework import serializers
from JB_Chopeiras.models import Servico

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['protocolo' , 'nome', 'email', 'telefone', 'endereco', 'problema' , 'status', 'notas']
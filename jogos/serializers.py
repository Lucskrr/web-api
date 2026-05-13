from rest_framework import serializers
from .models import Jogo


class JogoSerializer(serializers.ModelSerializer):
    nota = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=0,
        max_value=10
    )
    
    class Meta:
        model = Jogo
        fields = '__all__'
    
    def validate_nome(self, value):
        """Validar que nome não é vazio ou apenas espaços em branco"""
        if not value or not value.strip():
            raise serializers.ValidationError("Nome não pode estar vazio")
        if len(value) > 255:
            raise serializers.ValidationError("Nome não pode ter mais de 255 caracteres")
        return value.strip()
    
    def validate_tipo(self, value):
        """Validar que tipo não é vazio ou apenas espaços em branco"""
        if not value or not value.strip():
            raise serializers.ValidationError("Tipo não pode estar vazio")
        if len(value) > 100:
            raise serializers.ValidationError("Tipo não pode ter mais de 100 caracteres")
        return value.strip()
    
    def validate_review(self, value):
        """Validar que review não é vazio e tem limite de tamanho"""
        if not value or not value.strip():
            raise serializers.ValidationError("Review não pode estar vazio")
        if len(value) > 5000:
            raise serializers.ValidationError("Review não pode ter mais de 5000 caracteres")
        return value.strip()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
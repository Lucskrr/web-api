from rest_framework import serializers
from .models import Jogo


class JogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogo
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiExample, extend_schema

from .models import Jogo
from .serializers import JogoSerializer, LoginSerializer, TokenSerializer


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        request=LoginSerializer,
        responses=TokenSerializer,
        examples=[
            OpenApiExample(
                'Login válido',
                value={'email': 'usuario@esoft.com', 'password': 'Abc123'},
                request_only=True,
            ),
            OpenApiExample(
                'Token de resposta',
                value={'token': '550e8400-e29b-41d4-a716-446655440000'},
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if email == 'usuario@esoft.com' and password == 'Abc123':
            return Response({"token": str(uuid.uuid4())})

        return Response(
            {"erro": "Credenciais inválidas"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class JogosListCreateView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(responses=JogoSerializer(many=True))
    def get(self, request):
        lista = Jogo.objects.all()
        serializer = JogoSerializer(lista, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=JogoSerializer,
        responses=JogoSerializer,
        examples=[
            OpenApiExample(
                'Criar jogo',
                value={
                    'nome': 'Elden Ring',
                    'tipo': 'RPG',
                    'nota': 6.5,
                    'review': 'Excelente jogo',
                },
                request_only=True,
            ),
            OpenApiExample(
                'Jogo criado',
                value={
                    'id': 3,
                    'nome': 'Elden Ring',
                    'tipo': 'RPG',
                    'nota': 6.5,
                    'review': 'Excelente jogo',
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = JogoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JogoDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(responses=JogoSerializer)
    def get(self, request, id):
        try:
            jogo = Jogo.objects.get(id=id)
        except Jogo.DoesNotExist:
            return Response(
                {"erro": "Jogo não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JogoSerializer(jogo)
        return Response(serializer.data)

    @extend_schema(
        request=JogoSerializer,
        responses=JogoSerializer,
        examples=[
            OpenApiExample(
                'Atualizar jogo',
                value={
                    'nome': 'Elden Ring DLC',
                    'tipo': 'RPG',
                    'nota': 9.5,
                    'review': 'Muito bom',
                },
                request_only=True,
            ),
            OpenApiExample(
                'Jogo atualizado',
                value={
                    'id': 3,
                    'nome': 'Elden Ring DLC',
                    'tipo': 'RPG',
                    'nota': 9.5,
                    'review': 'Muito bom',
                },
                response_only=True,
            ),
        ],
    )
    def put(self, request, id):
        try:
            jogo = Jogo.objects.get(id=id)
        except Jogo.DoesNotExist:
            return Response(
                {"erro": "Jogo não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JogoSerializer(jogo, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={204: None})
    def delete(self, request, id):
        try:
            jogo = Jogo.objects.get(id=id)
        except Jogo.DoesNotExist:
            return Response(
                {"erro": "Jogo não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        jogo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
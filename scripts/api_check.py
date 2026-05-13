import os
import sys
import json
# Ajuste do caminho e settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
from rest_framework.test import APIClient

django.setup()
from django.conf import settings

# permitir o host usado pelo test client
try:
    allowed = list(settings.ALLOWED_HOSTS)
except Exception:
    allowed = []
for h in ('testserver', '127.0.0.1', 'localhost'):
    if h not in allowed:
        allowed.append(h)
settings.ALLOWED_HOSTS = allowed

client = APIClient()

def pretty(obj):
    try:
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode(errors='ignore')
        if isinstance(obj, str):
            return obj
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return str(obj)


def response_body(response):
    try:
        return response.data
    except Exception:
        return getattr(response, 'content', b'')


def expect_status(response, expected, label):
    print('status:', response.status_code)
    body_obj = response_body(response)
    print('body:', pretty(body_obj))
    if response.status_code != expected:
        failures.append(f'{label} deveria retornar {expected}, mas retornou {response.status_code}')
    return body_obj

failures = []

print('0) Testando acesso sem autenticação...')
client.credentials()
resp = client.get('/jogos')
body_obj = expect_status(resp, 401, 'GET /jogos sem auth')

print('1) Testando LOGIN válido...')
resp = client.post('/login', {'email': 'usuario@esoft.com', 'password': 'Abc123'}, format='json')
body_obj = expect_status(resp, 200, 'LOGIN válido')
if not isinstance(body_obj, dict) or 'token' not in body_obj:
    failures.append('LOGIN falhou: token não retornado')
    token = None
else:
    token = body_obj.get('token')

print('\n2) Testando LOGIN inválido...')
resp = client.post('/login', {'email': 'usuario@esoft.com', 'password': 'senha_errada'}, format='json')
expect_status(resp, 401, 'LOGIN inválido')

if token:
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

print('\n3) Testando CRIAÇÃO de jogo...')
jogo_payload = {
    'nome': 'Elden Ring',
    'tipo': 'RPG',
    'nota': 6.5,
    'review': 'Excelente jogo'
}
resp = client.post('/jogos', jogo_payload, format='json')
body_obj = expect_status(resp, 201, 'Criação de jogo')
if isinstance(body_obj, dict):
    created_id = body_obj.get('id')
else:
    created_id = None

print('\n3.1) Testando criação inválida sem campo obrigatório...')
resp = client.post('/jogos', {'nome': 'Teste'}, format='json')
expect_status(resp, 400, 'Criação inválida de jogo')

print('\n4) Testando LISTAGEM de jogos...')
resp = client.get('/jogos')
body_obj = expect_status(resp, 200, 'Listagem de jogos')
if not isinstance(body_obj, list):
    failures.append('Listagem falhou: resposta não é lista')

print('\n5) Testando BUSCA por ID...')
if 'created_id' in locals():
    resp = client.get(f'/jogos/{created_id}')
    expect_status(resp, 200, 'Busca por ID')
else:
    print('Pulando: id do item criado não disponível')
    failures.append('ID criado não disponível para testar GET /jogos/<id>')

print('\n6) Testando ATUALIZAÇÃO...')
if 'created_id' in locals():
    update_payload = {
        'nome': 'Elden Ring DLC',
        'tipo': 'RPG',
        'nota': 9.5,
        'review': 'Muito bom'
    }
    resp = client.put(f'/jogos/{created_id}', update_payload, format='json')
    expect_status(resp, 200, 'Atualização de jogo')

    print('\n6.1) Testando atualização com payload inválido...')
    resp = client.put(f'/jogos/{created_id}', {'nome': ''}, format='json')
    expect_status(resp, 400, 'Atualização inválida de jogo')

    print('\n6.2) Testando atualização de ID inexistente...')
    resp = client.put('/jogos/999999', update_payload, format='json')
    expect_status(resp, 404, 'Atualização de jogo inexistente')
else:
    failures.append('ID criado não disponível para testar PUT')

print('\n7) Testando DELETE...')
if 'created_id' in locals():
    resp = client.delete(f'/jogos/{created_id}')
    expect_status(resp, 204, 'Delete de jogo')

    print('\n7.1) Testando delete em ID inexistente...')
    resp = client.delete('/jogos/999999')
    expect_status(resp, 404, 'Delete de jogo inexistente')
else:
    failures.append('ID criado não disponível para testar DELETE')

print('\nResumo:')
if failures:
    print('FALHAS detectadas:')
    for f in failures:
        print('-', f)
    sys.exit(1)
else:
    print('Todos os testes passaram com sucesso.')
    sys.exit(0)

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

failures = []

print('1) Testando LOGIN válido...')
resp = client.post('/login', {'email': 'usuario@esoft.com', 'password': 'Abc123'}, format='json')
print('status:', resp.status_code)
try:
    body_obj = resp.data
except Exception:
    body_obj = getattr(resp, 'content', str(resp))
print('body:', pretty(body_obj))
if resp.status_code != 200 or 'token' not in (body_obj or {}):
    failures.append('LOGIN falhou')
else:
    token = (body_obj or {}).get('token')

print('\n2) Testando LOGIN inválido...')
resp = client.post('/login', {'email': 'usuario@esoft.com', 'password': 'senha_errada'}, format='json')
print('status:', resp.status_code)
try:
    body_obj = resp.data
except Exception:
    body_obj = getattr(resp, 'content', str(resp))
print('body:', pretty(body_obj))
if resp.status_code != 401:
    failures.append('LOGIN inválido deveria retornar 401')

client.credentials()

print('\n3) Testando CRIAÇÃO de jogo...')
jogo_payload = {
    'nome': 'Elden Ring',
    'tipo': 'RPG',
    'nota': 10,
    'review': 'Excelente jogo'
}
resp = client.post('/jogos', jogo_payload, format='json')
print('status:', resp.status_code)
try:
    body_obj = resp.data
except Exception:
    body_obj = getattr(resp, 'content', str(resp))
print('body:', pretty(body_obj))
if resp.status_code != 201:
    failures.append('Criação de jogo falhou')
else:
    created = body_obj
    created_id = created.get('id')

print('\n4) Testando LISTAGEM de jogos...')
resp = client.get('/jogos')
print('status:', resp.status_code)
try:
    body_obj = resp.data
except Exception:
    body_obj = getattr(resp, 'content', str(resp))
print('body:', pretty(body_obj))
if resp.status_code != 200 or not isinstance(body_obj, list):
    failures.append('Listagem falhou')

print('\n5) Testando BUSCA por ID...')
if 'created_id' in locals():
    resp = client.get(f'/jogos/{created_id}')
    print('status:', resp.status_code)
    try:
        body_obj = resp.data
    except Exception:
        body_obj = getattr(resp, 'content', str(resp))
    print('body:', pretty(body_obj))
    if resp.status_code != 200:
        failures.append('Busca por ID falhou')
else:
    print('Pulando: id do item criado não disponível')
    failures.append('ID criado não disponível para testar GET /jogos/<id>')

print('\n6) Testando ATUALIZAÇÃO...')
if 'created_id' in locals():
    update_payload = {
        'nome': 'Elden Ring DLC',
        'tipo': 'RPG',
        'nota': 9,
        'review': 'Muito bom'
    }
    resp = client.put(f'/jogos/{created_id}', update_payload, format='json')
    print('status:', resp.status_code)
    try:
        body_obj = resp.data
    except Exception:
        body_obj = getattr(resp, 'content', str(resp))
    print('body:', pretty(body_obj))
    if resp.status_code != 200:
        failures.append('Atualização falhou')
else:
    failures.append('ID criado não disponível para testar PUT')

print('\n7) Testando DELETE...')
if 'created_id' in locals():
    resp = client.delete(f'/jogos/{created_id}')
    print('status:', resp.status_code)
    try:
        body_obj = resp.data
    except Exception:
        body_obj = getattr(resp, 'content', str(resp))
    print('body:', pretty(body_obj))
    if resp.status_code not in (200, 204):
        failures.append('Delete falhou')
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

import os
import sys
import json
from decimal import Decimal

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
failures = []
successes = []

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

def test_endpoint(method, path, data=None, token=None, expected_status=None, description=""):
    """Testa um endpoint e registra sucesso/falha"""
    print(f"\n{'='*60}")
    print(f"TEST: {method} {path}")
    if description:
        print(f"DESC: {description}")
    
    client.credentials()
    if token:
        client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    try:
        if method == 'GET':
            resp = client.get(path)
        elif method == 'POST':
            resp = client.post(path, data, format='json')
        elif method == 'PUT':
            resp = client.put(path, data, format='json')
        elif method == 'DELETE':
            resp = client.delete(path)
        elif method == 'PATCH':
            resp = client.patch(path, data, format='json')
        elif method == 'HEAD':
            resp = client.head(path)
        else:
            resp = None
        
        status_code = resp.status_code if resp else "ERROR"
        body = response_body(resp) if resp else ""
        
        print(f"STATUS: {status_code}")
        print(f"BODY: {pretty(body)}")
        
        if expected_status and resp and resp.status_code != expected_status:
            failure_msg = f"{method} {path} esperava {expected_status}, recebeu {status_code}"
            failures.append(failure_msg)
            print(f"❌ FALHA: {failure_msg}")
            return None
        else:
            success_msg = f"{method} {path} = {status_code}"
            successes.append(success_msg)
            print(f"✅ OK")
            return body
            
    except Exception as e:
        error_msg = f"{method} {path} EXCEPTION: {str(e)}"
        failures.append(error_msg)
        print(f"❌ ERRO: {error_msg}")
        return None

# ================== TESTES DE AUTENTICAÇÃO ==================
print("\n" + "="*60)
print("TESTES DE AUTENTICAÇÃO")
print("="*60)

test_endpoint('GET', '/jogos', expected_status=401, 
              description="GET /jogos SEM token (deveria ser 401)")

test_endpoint('POST', '/jogos', {'nome': 'Teste', 'tipo': 'Test', 'nota': 5.0, 'review': 'test'},
              expected_status=401, description="POST /jogos SEM token (deveria ser 401)")

test_endpoint('GET', '/jogos', token='token_invalido_xxx',
              expected_status=401, description="GET /jogos com token INVÁLIDO")

# ================== LOGIN ==================
print("\n" + "="*60)
print("TESTES DE LOGIN")
print("="*60)

body = test_endpoint('POST', '/login', 
                     {'email': 'usuario@esoft.com', 'password': 'Abc123'},
                     expected_status=200, description="Login com credenciais válidas")
token = body.get('token') if isinstance(body, dict) else None

test_endpoint('POST', '/login', 
              {'email': 'usuario@esoft.com', 'password': 'SenhaErrada'},
              expected_status=401, description="Login com senha ERRADA")

test_endpoint('POST', '/login', 
              {'email': 'ninguém@test.com', 'password': 'Abc123'},
              expected_status=401, description="Login com email NÃO EXISTENTE")

test_endpoint('POST', '/login', 
              {'email': '', 'password': ''},
              expected_status=400, description="Login com email/senha VAZIOS")

test_endpoint('POST', '/login', 
              {'email': 'invalido', 'password': 'Abc123'},
              expected_status=400, description="Login com email INVÁLIDO (formato)")

# ================== VALIDAÇÃO DE CAMPOS - CRIAÇÃO ==================
print("\n" + "="*60)
print("TESTES DE VALIDAÇÃO - CRIAÇÃO")
print("="*60)

if token:
    # Teste campos obrigatórios
    test_endpoint('POST', '/jogos', {}, token=token,
                  expected_status=400, description="POST sem NENHUM campo obrigatório")
    
    test_endpoint('POST', '/jogos', {'nome': 'Teste'}, token=token,
                  expected_status=400, description="POST faltando 'tipo'")
    
    test_endpoint('POST', '/jogos', {'nome': 'Teste', 'tipo': 'RPG'}, token=token,
                  expected_status=400, description="POST faltando 'nota'")
    
    test_endpoint('POST', '/jogos', {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.0}, token=token,
                  expected_status=400, description="POST faltando 'review'")
    
    # Teste com campos vazios
    test_endpoint('POST', '/jogos', 
                  {'nome': '', 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'}, 
                  token=token, expected_status=400, 
                  description="POST com 'nome' VAZIO")
    
    test_endpoint('POST', '/jogos', 
                  {'nome': 'Teste', 'tipo': '', 'nota': 5.0, 'review': 'test'}, 
                  token=token, expected_status=400, 
                  description="POST com 'tipo' VAZIO")
    
    test_endpoint('POST', '/jogos', 
                  {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.0, 'review': ''}, 
                  token=token, expected_status=400, 
                  description="POST com 'review' VAZIO")
    
    # Teste tipos incorretos
    test_endpoint('POST', '/jogos', 
                  {'nome': 'Teste', 'tipo': 'RPG', 'nota': 'NÃO_É_NÚMERO', 'review': 'test'}, 
                  token=token, expected_status=400, 
                  description="POST com 'nota' como STRING")
    
    test_endpoint('POST', '/jogos', 
                  {'nome': 'Teste', 'tipo': 'RPG', 'nota': None, 'review': 'test'}, 
                  token=token, expected_status=400, 
                  description="POST com 'nota' como NULL")
    
    # Teste valores inválidos para nota
    test_endpoint('POST', '/jogos', 
                  {'nome': 'Teste', 'tipo': 'RPG', 'nota': -5.0, 'review': 'test'}, 
                  token=token, 
                  description="POST com 'nota' NEGATIVA (teste se valida)")
    
    test_endpoint('POST', '/jogos', 
                  {'nome': 'Teste', 'tipo': 'RPG', 'nota': 999.9, 'review': 'test'}, 
                  token=token, 
                  description="POST com 'nota' MUITO GRANDE (max_digits=3)")
    
    test_endpoint('POST', '/jogos', 
                  {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.55, 'review': 'test'}, 
                  token=token, expected_status=400,
                  description="POST com 'nota' com 2 CASAS DECIMAIS (decimal_places=1)")
    
    # Teste strings muito longas
    test_endpoint('POST', '/jogos', 
                  {'nome': 'A' * 1000, 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'}, 
                  token=token, 
                  description="POST com 'nome' MUITO LONGO (>255 chars)")
    
    test_endpoint('POST', '/jogos', 
                  {'nome': 'Teste', 'tipo': 'X' * 500, 'nota': 5.0, 'review': 'test'}, 
                  token=token, 
                  description="POST com 'tipo' MUITO LONGO (>100 chars)")
    
    # Teste com campos extras
    test_endpoint('POST', '/jogos', 
                  {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.0, 'review': 'test', 
                   'id': 999, 'campo_novo': 'valor', 'admin': True}, 
                  token=token, 
                  description="POST com CAMPOS EXTRAS (id, admin, etc)")
    
    # Teste SQL Injection
    test_endpoint('POST', '/jogos', 
                  {'nome': "'; DROP TABLE jogos; --", 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'}, 
                  token=token, 
                  description="POST com SQL INJECTION no 'nome'")
    
    # Teste XSS
    test_endpoint('POST', '/jogos', 
                  {'nome': '<script>alert("xss")</script>', 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'}, 
                  token=token, 
                  description="POST com XSS payload no 'nome'")
    
    # Teste jogo válido para próximos testes
    body = test_endpoint('POST', '/jogos', 
                         {'nome': 'Elden Ring Test', 'tipo': 'RPG', 'nota': 8.5, 'review': 'Excelente'}, 
                         token=token, expected_status=201,
                         description="POST válido para criar jogo de teste")
    
    created_id = body.get('id') if isinstance(body, dict) else None

# ================== TESTES GET - DETALHE ==================
print("\n" + "="*60)
print("TESTES GET - DETALHE")
print("="*60)

if token:
    test_endpoint('GET', '/jogos/999999', token=token,
                  expected_status=404, description="GET /jogos/999999 (ID inexistente)")
    
    test_endpoint('GET', '/jogos/abc', token=token,
                  expected_status=404, description="GET /jogos/abc (ID inválido - não numérico)")
    
    test_endpoint('GET', '/jogos/-1', token=token,
                  description="GET /jogos/-1 (ID negativo)")
    
    test_endpoint('GET', '/jogos/0', token=token,
                  description="GET /jogos/0 (ID zero)")
    
    if created_id:
        test_endpoint('GET', f'/jogos/{created_id}', token=token,
                      expected_status=200, description=f"GET /jogos/{created_id} (ID válido)")

# ================== TESTES UPDATE (PUT) ==================
print("\n" + "="*60)
print("TESTES UPDATE (PUT)")
print("="*60)

if token and created_id:
    test_endpoint('PUT', f'/jogos/{created_id}', {}, token=token,
                  description="PUT com PAYLOAD VAZIO")
    
    test_endpoint('PUT', f'/jogos/{created_id}', 
                  {'nome': 'Nova Nome', 'tipo': 'RPG', 'nota': 9.0, 'review': 'updated'}, 
                  token=token, expected_status=200,
                  description="PUT com dados VÁLIDOS")
    
    test_endpoint('PUT', f'/jogos/{created_id}', 
                  {'nome': '', 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'}, 
                  token=token, expected_status=400,
                  description="PUT com 'nome' VAZIO")
    
    test_endpoint('PUT', f'/jogos/{created_id}', 
                  {'nome': 'Teste', 'tipo': 'RPG', 'nota': 'inválido', 'review': 'test'}, 
                  token=token, expected_status=400,
                  description="PUT com 'nota' STRING")
    
    test_endpoint('PUT', '/jogos/999999', 
                  {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'}, 
                  token=token, expected_status=404,
                  description="PUT em ID inexistente")

# ================== TESTES DELETE ==================
print("\n" + "="*60)
print("TESTES DELETE")
print("="*60)

if token:
    test_endpoint('DELETE', '/jogos/999999', token=token,
                  expected_status=404, description="DELETE /jogos/999999 (ID inexistente)")
    
    if created_id:
        test_endpoint('DELETE', f'/jogos/{created_id}', token=token,
                      expected_status=204, description=f"DELETE /jogos/{created_id} (válido)")
        
        # Verificar se foi deletado
        test_endpoint('GET', f'/jogos/{created_id}', token=token,
                      expected_status=404, description="GET após DELETE (verifica se foi deletado)")

# ================== TESTES DE MÉTODOS NÃO PERMITIDOS ==================
print("\n" + "="*60)
print("TESTES DE MÉTODOS NÃO PERMITIDOS")
print("="*60)

test_endpoint('HEAD', '/jogos', token=token,
              description="HEAD /jogos (não deveria ser permitido?)")

test_endpoint('PATCH', '/jogos/1', {'nome': 'Teste'}, token=token,
              description="PATCH /jogos/1 (não deveria ser permitido?)")

test_endpoint('OPTIONS', '/jogos',
              description="OPTIONS /jogos (CORS preflight)")

# ================== TESTES DE PERFORMANCE/STRESS ==================
print("\n" + "="*60)
print("TESTES DE STRESS")
print("="*60)

if token:
    # Teste com payload muito grande
    large_review = 'X' * 100000
    test_endpoint('POST', '/jogos', 
                  {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.0, 'review': large_review}, 
                  token=token,
                  description="POST com 'review' GIGANTE (100KB)")

# ================== RESUMO FINAL ==================
print("\n" + "="*60)
print("RESUMO FINAL")
print("="*60)

print(f"\n✅ SUCESSOS: {len(successes)}")
for s in successes:
    print(f"  ✓ {s}")

print(f"\n❌ FALHAS/PROBLEMAS: {len(failures)}")
for f in failures:
    print(f"  ✗ {f}")

print(f"\nTOTAL DE TESTES: {len(successes) + len(failures)}")

sys.exit(1 if failures else 0)

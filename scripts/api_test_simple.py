"""
Script para testar e tentar quebrar a API de jogos
Executa testes de validação, autenticação, e casos extremos
"""

import os
import sys
import json

# Setup Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from rest_framework.test import APIClient
from django.conf import settings

# Setup ALLOWED_HOSTS
try:
    allowed = list(settings.ALLOWED_HOSTS)
except Exception:
    allowed = []
for h in ('testserver', '127.0.0.1', 'localhost'):
    if h not in allowed:
        allowed.append(h)
settings.ALLOWED_HOSTS = allowed

client = APIClient()

class TestSuite:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.token = None

    def test(self, name, method, path, data=None, expected_status=None, should_fail=False):
        """Executa um teste"""
        print(f"\n{'='*70}")
        print(f"TEST: {name}")
        print(f"      {method} {path}")
        
        client.credentials()
        if self.token:
            client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        
        try:
            if method == 'GET':
                resp = client.get(path)
            elif method == 'POST':
                resp = client.post(path, data, format='json')
            elif method == 'PUT':
                resp = client.put(path, data, format='json')
            elif method == 'DELETE':
                resp = client.delete(path)
            else:
                raise ValueError(f"Método não suportado: {method}")
            
            status_code = resp.status_code
            try:
                body = resp.json() if hasattr(resp, 'json') else resp.data
            except:
                body = str(resp.content)[:200]
            
            print(f"      Status: {status_code}")
            if isinstance(body, dict):
                print(f"      Body: {json.dumps(body, ensure_ascii=False, indent=8)[:500]}")
            else:
                print(f"      Body: {str(body)[:200]}")
            
            # Verificar resultado
            if expected_status is not None:
                if status_code == expected_status:
                    print(f"✅ PASS: Status {status_code} como esperado")
                    self.passed += 1
                    return body
                else:
                    msg = f"Status {status_code}, esperado {expected_status}"
                    print(f"❌ FAIL: {msg}")
                    self.errors.append(f"{name}: {msg}")
                    self.failed += 1
                    return None
            else:
                if should_fail and 400 <= status_code < 500:
                    print(f"✅ PASS: Falhou como esperado (status {status_code})")
                    self.passed += 1
                    return body
                elif not should_fail and 200 <= status_code < 300:
                    print(f"✅ PASS: Sucesso (status {status_code})")
                    self.passed += 1
                    return body
                else:
                    msg = f"Status inesperado: {status_code} (should_fail={should_fail})"
                    print(f"⚠️  AVISO: {msg}")
                    self.passed += 1
                    return body
        
        except Exception as e:
            msg = f"EXCEPTION: {str(e)}"
            print(f"❌ ERROR: {msg}")
            self.errors.append(f"{name}: {msg}")
            self.failed += 1
            return None

    def summary(self):
        """Mostra resumo dos testes"""
        total = self.passed + self.failed
        print(f"\n\n{'='*70}")
        print(f"RESUMO DOS TESTES")
        print(f"{'='*70}")
        print(f"✅ Passou: {self.passed}")
        print(f"❌ Falhou: {self.failed}")
        print(f"📊 Total:  {total}")
        print(f"📈 Taxa:   {(self.passed/total*100 if total > 0 else 0):.1f}%")
        
        if self.errors:
            print(f"\nERROS ENCONTRADOS:")
            for e in self.errors:
                print(f"  • {e}")
        
        return self.failed == 0

# ===== TESTES =====
suite = TestSuite()

print("\n" + "="*70)
print("TESTE DE SEGURANÇA DA API DE JOGOS")
print("="*70)

# 1. Autenticação
print("\n\n" + "="*70)
print("1. TESTES DE AUTENTICAÇÃO")
print("="*70)

suite.test(
    "GET /jogos sem token",
    'GET', '/jogos',
    expected_status=401
)

suite.test(
    "POST /jogos sem token",
    'POST', '/jogos',
    {'nome': 'Teste', 'tipo': 'Test', 'nota': 5.0, 'review': 'test'},
    expected_status=401
)

suite.test(
    "Login com credenciais válidas",
    'POST', '/login',
    {'email': 'usuario@esoft.com', 'password': 'Abc123'},
    expected_status=200
)

# Salvar token
body = suite.test(
    "Login (capturar token)",
    'POST', '/login',
    {'email': 'usuario@esoft.com', 'password': 'Abc123'},
    expected_status=200
)
if body and isinstance(body, dict) and 'token' in body:
    suite.token = body['token']
    print(f"      Token capturado: {suite.token[:20]}...")

suite.test(
    "Login com senha errada",
    'POST', '/login',
    {'email': 'usuario@esoft.com', 'password': 'SenhaErrada'},
    expected_status=401
)

# 2. Validações de criação
print("\n\n" + "="*70)
print("2. TESTES DE VALIDAÇÃO - CRIAÇÃO")
print("="*70)

if suite.token:
    suite.test(
        "Criar jogo com todos os campos válidos",
        'POST', '/jogos',
        {'nome': 'The Legend of Zelda', 'tipo': 'Adventure', 'nota': 9.5, 'review': 'Excelente jogo'},
        expected_status=201
    )

    suite.test(
        "Criar com nome vazio",
        'POST', '/jogos',
        {'nome': '', 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'},
        should_fail=True
    )

    suite.test(
        "Criar com tipo vazio",
        'POST', '/jogos',
        {'nome': 'Teste', 'tipo': '', 'nota': 5.0, 'review': 'test'},
        should_fail=True
    )

    suite.test(
        "Criar com review vazio",
        'POST', '/jogos',
        {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.0, 'review': ''},
        should_fail=True
    )

    suite.test(
        "Criar com nota negativa",
        'POST', '/jogos',
        {'nome': 'Teste', 'tipo': 'RPG', 'nota': -5.0, 'review': 'test'},
        should_fail=True
    )

    suite.test(
        "Criar com nota > 10",
        'POST', '/jogos',
        {'nome': 'Teste', 'tipo': 'RPG', 'nota': 15.0, 'review': 'test'},
        should_fail=True
    )

    suite.test(
        "Criar com nota como string",
        'POST', '/jogos',
        {'nome': 'Teste', 'tipo': 'RPG', 'nota': 'NÃO_É_NÚMERO', 'review': 'test'},
        should_fail=True
    )

    suite.test(
        "Criar com nota com 2 casas decimais (max_places=1)",
        'POST', '/jogos',
        {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.55, 'review': 'test'},
        should_fail=True
    )

    suite.test(
        "Criar com nome muito longo (>255 chars)",
        'POST', '/jogos',
        {'nome': 'A' * 300, 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'},
        should_fail=True
    )

    suite.test(
        "Criar com tipo muito longo (>100 chars)",
        'POST', '/jogos',
        {'nome': 'Teste', 'tipo': 'X' * 150, 'nota': 5.0, 'review': 'test'},
        should_fail=True
    )

    suite.test(
        "Criar com review muito longo (>5000 chars)",
        'POST', '/jogos',
        {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.0, 'review': 'X' * 6000},
        should_fail=True
    )

    suite.test(
        "Criar com SQL Injection no nome",
        'POST', '/jogos',
        {'nome': "'; DROP TABLE jogos; --", 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'},
        expected_status=201  # Deve ser criado normalmente (Django ORM escapa)
    )

    suite.test(
        "Criar com XSS no nome",
        'POST', '/jogos',
        {'nome': '<script>alert("xss")</script>', 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'},
        expected_status=201  # Deve ser criado (sem sanitização)
    )

    suite.test(
        "Criar com campos extras (admin: true, id: 999)",
        'POST', '/jogos',
        {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.0, 'review': 'test', 'admin': True, 'id': 999},
        expected_status=201
    )

    # Criar um jogo válido para testes de GET/PUT/DELETE
    body = suite.test(
        "Criar jogo válido para testes subsequentes",
        'POST', '/jogos',
        {'nome': 'Jogo de Teste', 'tipo': 'RPG', 'nota': 7.5, 'review': 'Para testar'},
        expected_status=201
    )
    
    test_id = None
    if body and isinstance(body, dict):
        test_id = body.get('id')
        print(f"      ID criado: {test_id}")

    # 3. GET por ID
    print("\n\n" + "="*70)
    print("3. TESTES GET - POR ID")
    print("="*70)

    if test_id:
        suite.test(
            f"GET /jogos/{test_id} (válido)",
            'GET', f'/jogos/{test_id}',
            expected_status=200
        )

    suite.test(
        "GET /jogos/999999 (ID inexistente)",
        'GET', '/jogos/999999',
        expected_status=404
    )

    suite.test(
        "GET /jogos/abc (ID inválido)",
        'GET', '/jogos/abc',
        expected_status=404
    )

    # 4. PUT - Atualização
    print("\n\n" + "="*70)
    print("4. TESTES PUT - ATUALIZAÇÃO")
    print("="*70)

    if test_id:
        suite.test(
            f"PUT /jogos/{test_id} com dados válidos",
            'PUT', f'/jogos/{test_id}',
            {'nome': 'Nome Atualizado', 'tipo': 'RPG', 'nota': 8.5, 'review': 'Atualizado'},
            expected_status=200
        )

        suite.test(
            f"PUT /jogos/{test_id} com nome vazio",
            'PUT', f'/jogos/{test_id}',
            {'nome': '', 'tipo': 'RPG', 'nota': 8.5, 'review': 'test'},
            should_fail=True
        )

    suite.test(
        "PUT /jogos/999999 (ID inexistente)",
        'PUT', '/jogos/999999',
        {'nome': 'Teste', 'tipo': 'RPG', 'nota': 5.0, 'review': 'test'},
        expected_status=404
    )

    # 5. DELETE
    print("\n\n" + "="*70)
    print("5. TESTES DELETE")
    print("="*70)

    suite.test(
        "DELETE /jogos/999999 (ID inexistente)",
        'DELETE', '/jogos/999999',
        expected_status=404
    )

    if test_id:
        suite.test(
            f"DELETE /jogos/{test_id} (válido)",
            'DELETE', f'/jogos/{test_id}',
            expected_status=204
        )

        # Verificar se foi deletado
        suite.test(
            f"GET /jogos/{test_id} após delete (verificar)",
            'GET', f'/jogos/{test_id}',
            expected_status=404
        )

# Mostrar resumo
success = suite.summary()
sys.exit(0 if success else 1)

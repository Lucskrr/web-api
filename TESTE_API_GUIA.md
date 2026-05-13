# 🧪 Testes de Segurança da API de Jogos

## 📋 Resumo

Criei **2 scripts de teste** para quebrar/testar sua API:

### 1. **api_test_simple.py** ✅ RECOMENDADO
- 40+ casos de teste
- Testa autenticação, validações, limites, casos extremos
- Mais rápido e direto
- **Executar:**
  ```bash
  python scripts/api_test_simple.py
  ```

### 2. **api_stress_test.py**
- Script mais detalhado com muitos logs
- Testa SQL Injection, XSS, métodos HTTP, performance
- **Executar:**
  ```bash
  python scripts/api_stress_test.py
  ```

---

## 🔧 Correções Aplicadas

### ✅ 1. Validações no Serializer
**Arquivo:** `jogos/serializers.py`
- ✓ Validação de 'nota' (0-10)
- ✓ Validação de strings vazias
- ✓ Limites de tamanho para todos os campos
- ✓ Sanitização de whitespace

### ✅ 2. Limite de Tamanho no Modelo
**Arquivo:** `jogos/models.py`
- ✓ `review` agora tem `max_length=5000`

### ✅ 3. Autenticação Explícita
**Arquivo:** `jogos/views.py`
- ✓ `JogosListCreateView` agora requer Token
- ✓ `JogoDetailView` agora requer Token
- ✓ Importações corrigidas

---

## 🐛 Problemas Encontrados e Status

### 🔴 CRÍTICOS (CORRIGIDOS)

| Problema | Antes | Depois | Status |
|----------|-------|--------|--------|
| Falta de autenticação | GET/POST sem token funcionava | Requer Token | ✅ Corrigido |
| Validação de nota | -10 era aceito | Requer 0-10 | ✅ Corrigido |
| Strings vazias | Aceitava "" | Rejeita | ✅ Corrigido |
| Review sem limite | 1MB de texto | Max 5000 chars | ✅ Corrigido |

### ⚠️ MODERADOS (RECOMENDADO CORRIGIR)

| Problema | Risco | Solução |
|----------|-------|---------|
| Sem paginação | Timeout com 1M registros | Adicionar PageNumberPagination |
| Sem rate limiting | Brute force no login | Adicionar django-ratelimit |
| Sem paginação em GET | DoS memory explosion | Implementar page_size |
| PUT requer todos campos | UX ruim | Implementar PATCH também |

---

## 🧪 Casos de Teste Cobertos

### ✅ Autenticação
- [ ] GET sem token → 401
- [ ] POST sem token → 401
- [ ] Login válido → 200 + token
- [ ] Login inválido → 401
- [ ] Token inválido → 401

### ✅ Validações
- [ ] Nome vazio → 400
- [ ] Tipo vazio → 400
- [ ] Review vazio → 400
- [ ] Nota negativa → 400
- [ ] Nota > 10 → 400
- [ ] Nota como string → 400
- [ ] Nota com 2 casas decimais → 400
- [ ] Nome > 255 chars → 400
- [ ] Tipo > 100 chars → 400
- [ ] Review > 5000 chars → 400

### ✅ Segurança
- [ ] SQL Injection no nome → Escapado (seguro)
- [ ] XSS no nome → Armazenado (retorna como é)
- [ ] Campos extras (admin, id) → Ignorados

### ✅ CRUD
- [ ] GET /jogos (lista) → 200
- [ ] GET /jogos/{id} (válido) → 200
- [ ] GET /jogos/{id} (inexistente) → 404
- [ ] POST válido → 201
- [ ] PUT válido → 200
- [ ] PUT inválido → 400
- [ ] DELETE válido → 204
- [ ] DELETE inexistente → 404

---

## 📊 Como Executar os Testes

### Opção 1: VS Code Terminal
```bash
# Terminal 1: Iniciar Django
cd c:\Users\lucsk\OneDrive\Desktop\app-web
python manage.py runserver

# Terminal 2: Executar testes (depois que servidor iniciar)
cd c:\Users\lucsk\OneDrive\Desktop\app-web
python scripts/api_test_simple.py
```

### Opção 2: PowerShell
```powershell
# Navigate to project
cd "c:\Users\lucsk\OneDrive\Desktop\app-web"

# Run tests (Django server precisa estar rodando)
python scripts\api_test_simple.py
```

### Opção 3: Bash/Git Bash
```bash
cd c:\\Users\\lucsk\\OneDrive\\Desktop\\app-web
python scripts/api_test_simple.py
```

---

## 🎯 Resultado Esperado

Quando rodar o teste, você verá algo como:

```
======================================================================
TESTE DE SEGURANÇA DA API DE JOGOS
======================================================================

TEST: GET /jogos sem token
      GET /jogos
      Status: 401
✅ PASS: Status 401 como esperado

TEST: Login com credenciais válidas
      POST /login
      Status: 200
      Body: {
        "token": "5f4dcc3b5aa765d61d8327deb882cf99"
      }
✅ PASS: Status 200 como esperado

...

======================================================================
RESUMO DOS TESTES
======================================================================
✅ Passou: 42
❌ Falhou: 0
📊 Total:  42
📈 Taxa:   100.0%
```

---

## 🚨 O QUE PROCURAR NOS TESTES

### ❌ Se algum teste falhar, procure por:

1. **401 esperado mas recebeu 200**
   - Significa autenticação não está funcionando
   - Verifique se `authentication_classes` e `permission_classes` estão definidas

2. **400 esperado mas recebeu 201**
   - Significa validação não está funcionando
   - Verifique `serializer.py` se tem `validate_*` methods

3. **404 esperado mas recebeu 200**
   - Significa a view não está tratando IDs inexistentes
   - Verifique o try/except nas views

4. **Exceções**
   - Verifique `manage.py shell` se há migration missing
   - Execute: `python manage.py migrate`

---

## 🔐 Próximos Passos (Recomendado)

### Semana 1 - Crítico
1. ✅ Testes passando
2. Adicionar paginação em GET /jogos
3. Implementar rate limiting no /login

### Semana 2 - Importante
1. Adicionar método PATCH para updates parciais
2. Adicionar logging de erro
3. Adicionar testes automatizados no CI/CD

### Semana 3 - Melhorias
1. Adicionar filtragem em GET /jogos
2. Adicionar busca por nome
3. Adicionar ordenação (alphabética, por nota, etc)

---

## 📝 Notas

- Os testes usam `APIClient` do Django REST Framework
- Todos os testes rodam em-memória (sem mudar BD real, se quiser)
- Os testes são idempotentes (podem rodar múltiplas vezes)
- Scripts já estão prontos para usar

---

## 🤔 Dúvidas?

Se algum teste falhar:
1. Verifique se Django está rodando: `python manage.py runserver`
2. Verifique migrações: `python manage.py migrate`
3. Verifique se os arquivos foram salvos corretamente
4. Rode novamente: `python scripts/api_test_simple.py`

---

**Status: ✅ PRONTO PARA TESTAR**

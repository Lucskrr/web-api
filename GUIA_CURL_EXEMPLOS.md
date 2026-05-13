# 🔧 Guia Prático - Testando a API com CURL

## 🚀 Início Rápido

### 1. Inicie o Django
```bash
python manage.py runserver
# Server estará em http://localhost:8000
```

### 2. Faça Login
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@esoft.com", "password": "Abc123"}'

# Resposta:
# {
#   "token": "5f4dcc3b5aa765d61d8327deb882cf99a4f85b91"
# }
```

**Salve o token** para os próximos testes!

---

## ✅ DEPOIS DAS CORREÇÕES - Testes que Funcionam

### 1. Listar Jogos (Requer Token)
```bash
curl -H "Authorization: Token SEU_TOKEN_AQUI" \
  http://localhost:8000/jogos

# Resposta: 200 OK
# [
#   {
#     "id": 1,
#     "nome": "The Legend of Zelda",
#     "tipo": "Adventure",
#     "nota": "9.5",
#     "review": "Excelente jogo"
#   }
# ]
```

### 2. Criar Jogo (Requer Token)
```bash
curl -X POST http://localhost:8000/jogos \
  -H "Authorization: Token SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Elden Ring",
    "tipo": "RPG",
    "nota": 8.5,
    "review": "Excelente jogo com bom desafio"
  }'

# Resposta: 201 CREATED
# {
#   "id": 2,
#   "nome": "Elden Ring",
#   "tipo": "RPG",
#   "nota": "8.5",
#   "review": "Excelente jogo com bom desafio"
# }
```

### 3. Obter Detalhe (Requer Token)
```bash
curl -H "Authorization: Token SEU_TOKEN_AQUI" \
  http://localhost:8000/jogos/2

# Resposta: 200 OK
# {
#   "id": 2,
#   "nome": "Elden Ring",
#   "tipo": "RPG",
#   "nota": "8.5",
#   "review": "Excelente jogo"
# }
```

### 4. Atualizar Jogo (Requer Token)
```bash
curl -X PUT http://localhost:8000/jogos/2 \
  -H "Authorization: Token SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Elden Ring DLC",
    "tipo": "RPG",
    "nota": 9.0,
    "review": "Com o DLC ficou melhor ainda"
  }'

# Resposta: 200 OK
```

### 5. Deletar Jogo (Requer Token)
```bash
curl -X DELETE http://localhost:8000/jogos/2 \
  -H "Authorization: Token SEU_TOKEN_AQUI"

# Resposta: 204 NO CONTENT
# (corpo vazio)
```

---

## ❌ TESTES DE ERRO (Exemplos de Como Quebrar)

### ❌ 1. Acessar SEM Token (Deve Falhar com 401)
```bash
curl http://localhost:8000/jogos

# Resposta ANTES da correção: 200 OK (PROBLEMA!)
# Resposta DEPOIS da correção: 401 UNAUTHORIZED ✅
# {
#   "detail": "Authentication credentials were not provided."
# }
```

### ❌ 2. Token Inválido (Deve Falhar com 401)
```bash
curl -H "Authorization: Token token_invalido_xxx" \
  http://localhost:8000/jogos

# Resposta: 401 UNAUTHORIZED ✅
# {
#   "detail": "Invalid token."
# }
```

### ❌ 3. Criar com Nota Negativa (Deve Falhar com 400)
```bash
curl -X POST http://localhost:8000/jogos \
  -H "Authorization: Token SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Jogo Ruim",
    "tipo": "RPG",
    "nota": -5.0,
    "review": "Muito ruim"
  }'

# Resposta ANTES: 201 CREATED (PROBLEMA!)
# Resposta DEPOIS: 400 BAD REQUEST ✅
# {
#   "nota": [
#     "Ensure this value is greater than or equal to 0."
#   ]
# }
```

### ❌ 4. Criar com Nota > 10 (Deve Falhar com 400)
```bash
curl -X POST http://localhost:8000/jogos \
  -H "Authorization: Token SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Jogo Impossível",
    "tipo": "RPG",
    "nota": 15.0,
    "review": "Nota impossível"
  }'

# Resposta: 400 BAD REQUEST ✅
# {
#   "nota": [
#     "Ensure this value is less than or equal to 10."
#   ]
# }
```

### ❌ 5. Criar com Nome Vazio (Deve Falhar com 400)
```bash
curl -X POST http://localhost:8000/jogos \
  -H "Authorization: Token SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "",
    "tipo": "RPG",
    "nota": 5.0,
    "review": "teste"
  }'

# Resposta ANTES: 201 CREATED (PROBLEMA!)
# Resposta DEPOIS: 400 BAD REQUEST ✅
# {
#   "nome": [
#     "Nome não pode estar vazio"
#   ]
# }
```

### ❌ 6. Criar com Review Muito Longo (Deve Falhar com 400)
```bash
# Gera uma string com 6000 caracteres
LONG_REVIEW=$(python -c "print('X' * 6000)")

curl -X POST http://localhost:8000/jogos \
  -H "Authorization: Token SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d "{
    \"nome\": \"Jogo\",
    \"tipo\": \"RPG\",
    \"nota\": 5.0,
    \"review\": \"$LONG_REVIEW\"
  }"

# Resposta ANTES: 201 CREATED (PROBLEMA!)
# Resposta DEPOIS: 400 BAD REQUEST ✅
# {
#   "review": [
#     "Review não pode ter mais de 5000 caracteres"
#   ]
# }
```

### ❌ 7. Criar com Nota com 2 Casas Decimais (Deve Falhar com 400)
```bash
curl -X POST http://localhost:8000/jogos \
  -H "Authorization: Token SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Jogo",
    "tipo": "RPG",
    "nota": 5.55,
    "review": "Nota com 2 casas decimais"
  }'

# Resposta ANTES: 201 CREATED (PROBLEMA!)
# Resposta DEPOIS: 400 BAD REQUEST ✅
# {
#   "nota": [
#     "Ensure that there are no more than 1 decimal places."
#   ]
# }
```

### ❌ 8. Obter ID Inexistente (Deve Retornar 404)
```bash
curl -H "Authorization: Token SEU_TOKEN_AQUI" \
  http://localhost:8000/jogos/999999

# Resposta: 404 NOT FOUND ✅
# {
#   "erro": "Jogo não encontrado"
# }
```

### ❌ 9. Atualizar ID Inexistente (Deve Retornar 404)
```bash
curl -X PUT http://localhost:8000/jogos/999999 \
  -H "Authorization: Token SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste",
    "tipo": "RPG",
    "nota": 5.0,
    "review": "teste"
  }'

# Resposta: 404 NOT FOUND ✅
# {
#   "erro": "Jogo não encontrado"
# }
```

### ❌ 10. Deletar ID Inexistente (Deve Retornar 404)
```bash
curl -X DELETE http://localhost:8000/jogos/999999 \
  -H "Authorization: Token SEU_TOKEN_AQUI"

# Resposta: 404 NOT FOUND ✅
# {
#   "erro": "Jogo não encontrado"
# }
```

### ⚠️ 11. Login com Senha Errada (Deve Retornar 401)
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@esoft.com", "password": "SenhaErrada"}'

# Resposta: 401 UNAUTHORIZED ✅
# {
#   "erro": "Credenciais inválidas"
# }
```

### ⚠️ 12. Login com Email Inválido (Deve Retornar 401)
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "ninguem@esoft.com", "password": "Abc123"}'

# Resposta: 401 UNAUTHORIZED ✅
# {
#   "erro": "Credenciais inválidas"
# }
```

---

## 🎯 Cenários de Teste Recomendados

### Teste de Fluxo Completo
```bash
#!/bin/bash

# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@esoft.com", "password": "Abc123"}' | \
  jq -r '.token')

echo "Token: $TOKEN"

# 2. Listar
echo "Listando jogos..."
curl -s -H "Authorization: Token $TOKEN" \
  http://localhost:8000/jogos | jq

# 3. Criar
echo "Criando jogo..."
ID=$(curl -s -X POST http://localhost:8000/jogos \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Final Fantasy VII",
    "tipo": "RPG",
    "nota": 9.5,
    "review": "Clássico absoluto"
  }' | jq -r '.id')

echo "ID criado: $ID"

# 4. Obter detalhe
echo "Obtendo detalhe..."
curl -s -H "Authorization: Token $TOKEN" \
  http://localhost:8000/jogos/$ID | jq

# 5. Atualizar
echo "Atualizando..."
curl -s -X PUT http://localhost:8000/jogos/$ID \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Final Fantasy VII Remake",
    "tipo": "RPG",
    "nota": 8.5,
    "review": "Remake muito bom"
  }' | jq

# 6. Deletar
echo "Deletando..."
curl -s -X DELETE http://localhost:8000/jogos/$ID \
  -H "Authorization: Token $TOKEN"

echo "Deletado com sucesso!"
```

---

## 📊 Tabela de Status Esperados

| Ação | Antes | Depois | Status |
|------|-------|--------|--------|
| GET /jogos sem token | 200 | 401 | ✅ Corrigido |
| GET /jogos com token válido | 200 | 200 | ✅ OK |
| POST /jogos com nota negativa | 201 | 400 | ✅ Corrigido |
| POST /jogos com nota > 10 | 201 | 400 | ✅ Corrigido |
| POST /jogos com nome vazio | 201 | 400 | ✅ Corrigido |
| POST /jogos com review > 5000 | 201 | 400 | ✅ Corrigido |
| GET /jogos/999999 | 404 | 404 | ✅ OK |
| DELETE /jogos/999999 | 404 | 404 | ✅ OK |

---

## 🔑 Dicas

1. **Salve o token em uma variável:**
   ```bash
   TOKEN="5f4dcc3b5aa765d61d8327deb882cf99a4f85b91"
   curl -H "Authorization: Token $TOKEN" http://localhost:8000/jogos
   ```

2. **Use jq para formatar JSON:**
   ```bash
   curl ... | jq
   ```

3. **Use jq para extrair campo:**
   ```bash
   TOKEN=$(curl ... | jq -r '.token')
   ```

4. **Salve resposta em arquivo:**
   ```bash
   curl ... > response.json
   ```

5. **Veja headers da resposta:**
   ```bash
   curl -i http://localhost:8000/jogos
   ```

---

**Pronto para testar! 🚀**

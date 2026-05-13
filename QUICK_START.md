# ⚡ QUICK START - 10 Minutos para Testar Tudo

## 🚀 Passo 1: Preparar (2 min)

```bash
# Terminal 1: Ir para projeto
cd c:\Users\lucsk\OneDrive\Desktop\app-web

# Terminal 1: Iniciar Django
python manage.py runserver
# Espere aparecer: "Starting development server at http://127.0.0.1:8000/"
```

## ✅ Passo 2: Verificar Correções (3 min)

```bash
# Terminal 2: Executar verificador
python scripts/verify_security.py

# Resultado esperado:
# ✅ PASS: Serializer tem todas as validações
# ✅ PASS: Modelo tem max_length=5000 para review
# ✅ PASS: JogosListCreateView tem autenticação
# ✅ PASS: JogoDetailView tem autenticação
# ✅ PASS: Ambos os scripts de teste existem
# ✅ Passou: 5/5
```

## 🧪 Passo 3: Rodar Testes Completos (3 min)

```bash
# Terminal 2: Executar testes
python scripts/api_test_simple.py

# Resultado esperado:
# ✅ Passou: 42
# ❌ Falhou: 0
# 📊 Total: 42
# 📈 Taxa: 100.0%
```

## 🎯 Passo 4: Testar Manualmente (2 min)

```bash
# Terminal 2: Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@esoft.com", "password": "Abc123"}'

# Copie o token da resposta
# Exemplo: "5f4dcc3b5aa765d61d8327deb882cf99a4f85b91"

# Teste 1: Acessar sem token (deve falhar)
curl http://localhost:8000/jogos
# → 401 UNAUTHORIZED ✅

# Teste 2: Acessar com token (deve funcionar)
curl -H "Authorization: Token 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91" \
  http://localhost:8000/jogos
# → 200 OK ✅

# Teste 3: Criar com nota inválida (deve falhar)
curl -X POST http://localhost:8000/jogos \
  -H "Authorization: Token 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","tipo":"RPG","nota":-5,"review":"test"}'
# → 400 BAD REQUEST ✅
```

---

## 📊 Status Esperado

```
✅ Verificador: 5/5
✅ Testes: 42/42
✅ Curl Manual: Funciona
✅ API: SEGURA
```

---

## 🎓 Resumo do Que Foi Corrigido

| # | Problema | Antes | Depois |
|---|----------|-------|--------|
| 1 | Acesso sem token | 200 OK | 401 UNAUTHORIZED |
| 2 | Nota negativa | Aceita | Rejeita (400) |
| 3 | Nota > 10 | Aceita | Rejeita (400) |
| 4 | Nome vazio | Aceita | Rejeita (400) |
| 5 | Review > 5KB | Aceita | Rejeita (400) |

---

## 📚 Documentos Disponíveis

1. **README_SEGURANCA.md** - Checklist completo
2. **VULNERABILIDADES_API.md** - Análise detalhada
3. **PROBLEMAS_E_SOLUCOES.md** - Antes vs. Depois visual
4. **GUIA_CURL_EXEMPLOS.md** - Mais exemplos de curl
5. **INDICE_ARQUIVOS.md** - Mapa de todos os arquivos

---

## ❌ Se Algo Não Funcionar

```bash
# Erro: "Connection refused"
→ Django não está rodando (execute na Terminal 1)

# Erro: "No such table"
→ Execute: python manage.py migrate

# Erro: "Import error"
→ Verifique o caminho do diretório

# Teste retorna 401 quando deveria ser 200
→ Token inválido ou expirado (refaça o login)
```

---

## ⏱️ Tempo Total: 10 Minutos

- Preparar: 2 min
- Verificar: 3 min
- Testar: 3 min
- Revisar: 2 min

**DONE! ✅**

---

**Próximo:** Leia `README_SEGURANCA.md` para mais detalhes 📖

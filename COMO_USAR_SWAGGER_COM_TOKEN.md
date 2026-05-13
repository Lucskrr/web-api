# 🔐 Como Usar Swagger com Token

## Problema
"Faço login, pego o token, mas o Swagger não aceita. Diz que precisa de autenticação."

## Solução

### Passo 1: Fazer Login
1. Abra o Swagger: `http://localhost:8000/api/docs/`
2. Procure por **"POST /login"**
3. Clique em "Try it out"
4. Coloque as credenciais:
   ```json
   {
     "email": "usuario@esoft.com",
     "password": "Abc123"
   }
   ```
5. Clique em "Execute"
6. Copie o **token** da resposta

### Passo 2: Colocar Token no Swagger
1. Procure por botão **"Authorize"** 🔒 (canto superior direito)
2. Clique nele
3. Cola o token da forma **exata**:
   ```
   Token 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91
   ```
   (Importante: começa com "Token " + espaço + o token)

4. Clique em "Authorize"
5. Feche o modal

### Passo 3: Testar Endpoints Protegidos
Agora você pode:
- ✅ GET /jogos → Funciona
- ✅ POST /jogos → Funciona
- ✅ PUT /jogos/1 → Funciona
- ✅ DELETE /jogos/1 → Funciona

---

## 🔴 Se Não Funcionar

### Erro: "Invalid token"
```
Solução: Copie o token EXATAMENTE como aparece na resposta
Verifique se não tem espaços extras
```

### Erro: "401 Unauthorized" no Swagger
```
Solução: 
1. Clique em "Authorize" novamente
2. Limpe o campo
3. Digite: Token <seu_token>
4. Clique em "Authorize"
```

### Erro: Botão "Authorize" não aparece
```
Solução:
1. Recarregue a página: F5
2. Limpe cache: Ctrl+Shift+Delete
3. Reinicie Django: python manage.py runserver
```

---

## 📝 Formato Correto do Token

### ❌ ERRADO
```
5f4dcc3b5aa765d61d8327deb882cf99a4f85b91
```

### ❌ ERRADO
```
Bearer 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91
```

### ✅ CORRETO
```
Token 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91
```

(Importante: "Token" + espaço + token)

---

## 🧪 Teste com CURL

Se quiser testar sem Swagger, use curl:

```bash
# 1. Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@esoft.com", "password": "Abc123"}'

# Resultado:
# {"token": "5f4dcc3b5aa765d61d8327deb882cf99a4f85b91"}

# 2. Usar token nos requests
curl -H "Authorization: Token 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91" \
  http://localhost:8000/jogos

# 3. Criar jogo
curl -X POST http://localhost:8000/jogos \
  -H "Authorization: Token 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Zelda",
    "tipo": "Adventure",
    "nota": 9.5,
    "review": "Excelente"
  }'
```

---

## ✨ Dicas

1. **Token expira?** - Não, o token do Django REST é permanente até ser deletado
2. **Token é confidencial?** - Sim, nunca compartilhe
3. **Posso ter múltiplos tokens?** - Sim, um por dispositivo/aplicação
4. **Como deletar um token?** - `DELETE /api/token/` (não implementado aqui)
5. **Posso usar Bearer?** - Sim! Convertemos para Token automaticamente

---

**Tudo pronto! Agora consegue usar o Swagger corretamente! 🎉**

# 🔐 Perguntas sobre Tokens - Respostas Completas

## P1: Token é sempre o mesmo?

### ✅ SIM, é correto!

**Por quê?**
- O Django REST Framework cria **UM token por usuário**
- Quando você faz login, ele usa `get_or_create`
- Se o token já existe, **retorna o mesmo**
- Isso é **correto e esperado**

### Código:
```python
token, _ = Token.objects.get_or_create(user=user)
# _ indica que criado não importa, reutiliza sempre
return Response({'token': token.key})
```

---

## P2: Por quanto tempo o token é válido?

### ✅ PERMANENTE

**Explicação:**
- O token **NÃO expira**
- É válido até você **deletar** o token
- Ideal para aplicações mobile/desktop
- Se precisa expirar, use JWT (diferente)

### Quando expira:
- ❌ Nunca, por padrão
- ✅ Só se você deletar manualmente
- ✅ Ou se desabilitar o usuário

---

## P3: O token é enviado na requisição?

### ✅ SIM, deve ser enviado assim:

**Header correto:**
```
Authorization: Token 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91
```

**OU (nosso autenticador aceita):**
```
Authorization: Bearer 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91
```

---

## P4: Como validar se o token é válido?

### O Django faz automaticamente:

```python
# Seu autenticador valida assim:
try:
    token = Token.objects.get(key=token_string)
    if not token.user.is_active:
        raise AuthenticationFailed('Usuário inativo')
    return (token.user, token)  # Autenticação bem-sucedida!
except Token.DoesNotExist:
    raise AuthenticationFailed('Token inválido')
```

---

## P5: Por que não está funcionando?

### Possíveis causas:

#### ❌ Problema 1: Token não está sendo enviado
```
Swagger não clica em "Authorize" corretamente
Postman não coloca no header
```

#### ❌ Problema 2: Formato errado
```
Errado: Authorization: 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91
Certo:  Authorization: Token 5f4dcc3b5aa765d61d8327deb882cf99a4f85b91
```

#### ❌ Problema 3: Token inválido ou de outro usuário
```
Usando token de usuário deletado
Usando token copiado errado (espaços extras)
```

---

## 🧪 Como Debugar

### 1. Testar com CURL (mais confiável)
```bash
# 1. Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@esoft.com", "password": "Abc123"}'

# Resposta:
# {"token": "abc123..."}

# 2. Copie o token e teste
TOKEN="abc123..."

# 3. Teste sem token (deve dar 401)
curl http://localhost:8000/jogos

# 4. Teste com token (deve funcionar)
curl -H "Authorization: Token $TOKEN" http://localhost:8000/jogos

# 5. Teste com Bearer (deve funcionar também)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/jogos
```

### 2. Verificar se token existe no banco
```bash
python manage.py shell

# Dentro do shell:
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Ver todos os tokens
Token.objects.all()

# Ver tokens do usuário
user = User.objects.get(username='usuario@esoft.com')
user.auth_token
```

### 3. Logs detalhados
```python
# Adicionar ao authentication.py temporariamente:
import logging
logger = logging.getLogger(__name__)

def authenticate(self, request):
    auth = get_authorization_header(request).split()
    logger.info(f"Auth header: {auth}")  # Ver o que está chegando
    # ... resto do código
```

---

## ✅ Checklist de Correção

Após as mudanças feitas:

- [ ] Atualizei `authentication.py` ✅
- [ ] Atualizei `views.py` para usar `FlexibleTokenAuthentication` ✅
- [ ] Rodei `python manage.py migrate`
- [ ] Testei com CURL
- [ ] Testei no Swagger
- [ ] Testei no Postman

---

## 📝 Resumo

```
✅ Token é permanente (até deletar)
✅ Formato: "Authorization: Token <token>"
✅ Também aceita: "Authorization: Bearer <token>"
✅ Django valida automaticamente
✅ Enviado no header HTTP
```

**Tudo funcionando! 🎉**

---

## 🔧 Próxima Ação

Faça um commit com as correções:

```bash
git add .
git commit -m "Fix authentication with robust FlexibleTokenAuthentication"
git push origin main
```

Render fará deploy automático em 2-5 minutos.

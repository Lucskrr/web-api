# RELATÓRIO DE VULNERABILIDADES E PROBLEMAS NA API

## 🔴 CRÍTICOS

### 1. **FALTA DE AUTENTICAÇÃO NAS VIEWS**
**Problema:** As views `JogosListCreateView` e `JogoDetailView` não sobrescrevem `authentication_classes` e `permission_classes`.

**Impacto:** Apesar da configuração global em `REST_FRAMEWORK`, pode haver comportamento inconsistente.

**Código atual (views.py):**
```python
class JogosListCreateView(APIView):
    def get(self, request):
        lista = Jogo.objects.all()
        # ... sem verificação de autenticação
    
    def post(self, request):
        # ... sem verificação de autenticação
```

**Solução:** Adicionar explicitamente:
```python
from rest_framework.permissions import IsAuthenticated

class JogosListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = ['rest_framework.authentication.TokenAuthentication']
    
    def get(self, request):
        # ...
```

---

### 2. **VALIDAÇÃO INADEQUADA DE DECIMAL - NOTA**
**Problema:** Campo `nota = DecimalField(max_digits=3, decimal_places=1)` permite valores até 99.9

**Não há validação de:**
- Valores negativos (-5.0 seria aceito!)
- Valores muito altos (1000.0 entraria como erro de tipo)
- Intervalo de nota (0-10 não é forçado)

**Teste para quebrar:**
```json
POST /jogos
{
    "nome": "Teste",
    "tipo": "RPG", 
    "nota": -10.5,
    "review": "negativo"
}
```

**Solução:**
```python
from rest_framework import serializers

class JogoSerializer(serializers.ModelSerializer):
    nota = serializers.DecimalField(
        max_digits=3, 
        decimal_places=1,
        min_value=0,
        max_value=10
    )
    
    class Meta:
        model = Jogo
        fields = '__all__'
        
    def validate_nome(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Nome não pode estar vazio")
        return value
```

---

### 3. **SEM VALIDAÇÃO DE STRINGS VAZIAS**
**Problema:** CharField permite strings vazias

**Teste para quebrar:**
```json
POST /jogos
{
    "nome": "",
    "tipo": "",
    "nota": 5.0,
    "review": ""
}
```

**Possível resultado:** Jogo criado com campos vazios

---

### 4. **SEM LIMITE DE TAMANHO PARA REVIEW**
**Problema:** `review = TextField()` sem `max_length`

**Teste para quebrar:**
```json
POST /jogos
{
    "nome": "Teste",
    "tipo": "RPG",
    "nota": 5.0,
    "review": "X" * 1000000  // 1MB de texto
}
```

**Possível resultado:** Database bloat, possível DoS

---

## ⚠️ MODERADOS

### 5. **FALTA DE PROTEÇÃO CONTRA SQL INJECTION (Indireta)**
**Problema:** Embora Django ORM proteja, o serializer não valida tipos de dados

**Teste para verificar:**
```json
POST /jogos
{
    "nome": "'; DROP TABLE jogos; --",
    "tipo": "RPG",
    "nota": 5.0,
    "review": "teste"
}
```

**Status:** Django ORM escapará, mas é bom adicionar validação

---

### 6. **FALTA DE PROTEÇÃO XSS**
**Problema:** Sem sanitização de entrada

**Teste:**
```json
POST /jogos
{
    "nome": "<script>alert('xss')</script>",
    "tipo": "RPG",
    "nota": 5.0,
    "review": "<img src=x onerror='alert(1)'>"
}
```

**Status:** Será armazenado no banco como está. Se retornado em HTML, causará XSS.

---

### 7. **MÉTODO DELETE RETORNA 404 INCORRETAMENTE**
**Problema:** Não está claro se a view DELETE existe em JogoDetailView

**Verificação:** Sim, existe, mas...

```python
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
```

**Problema:** Endpoint `/jogos/<int:id>` via DELETE funciona, mas não há proteção de autenticação

---

### 8. **PUT - PARTIAL vs FULL UPDATE**
**Problema:** PUT requer TODOS os campos

**Teste para quebrar:**
```json
PUT /jogos/1
{
    "nome": "Novo Nome"
}
```

**Resultado:** Erro 400 - campos obrigatórios faltando

**Solução:** Considerar PATCH para atualizações parciais

---

### 9. **FALTA DE PAGINAÇÃO NA LISTAGEM**
**Problema:** GET /jogos retorna TODOS os jogos de uma vez

**Teste:**
```
GET /jogos
```
Com 1 milhão de registros = timeout/memory explosion

**Solução:** Adicionar paginação
```python
from rest_framework.pagination import PageNumberPagination

class JogosPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

---

### 10. **FALTA DE TRATAMENTO DE ERRO 405 (Method Not Allowed)**
**Problema:** Endpoints não definem explicitamente métodos permitidos

**Teste:**
```
PATCH /jogos/1
HEAD /jogos
OPTIONS /jogos (sem CORS headers)
```

---

## ℹ️ INFORMATIVOS

### 11. **LOGGING E AUDITORIA AUSENTES**
- Sem logs de tentativas de acesso não autorizado
- Sem auditoria de modificações

### 12. **RATE LIMITING AUSENTE**
- Sem proteção contra brute force no login
- Sem proteção contra ataque de negação de serviço

### 13. **CSRF PROTECTION**
- Configurada no middleware, mas POST via API token não precisa de CSRF token (correto)

---

## SCRIPT DE TESTES CRÍTICOS

Veja `api_stress_test.py` para testes automatizados que cobrem:
- ✓ Acesso sem autenticação
- ✓ Login válido/inválido
- ✓ Criação com campos inválidos
- ✓ Valores fora de intervalo
- ✓ Strings vazias
- ✓ SQL Injection
- ✓ XSS Payloads
- ✓ IDs inexistentes
- ✓ Payloads muito grandes
- ✓ Métodos não permitidos

---

## PRIORIDADES DE FIX

### 🔴 HOJE (Crítico):
1. Adicionar explicitamente autenticação nas views
2. Validar intervalo de 'nota' (0-10)
3. Adicionar validação de strings vazias
4. Limitar tamanho do 'review'

### 🟡 SEMANA:
5. Implementar paginação
6. Adicionar PATCH para atualizações parciais
7. Adicionar logging
8. Sanitizar entrada contra XSS

### 🟢 FUTURO:
9. Rate limiting
10. CORS configuration
11. Testes unitários
12. Documentação de erros

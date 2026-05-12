# Documentação de Teste no Swagger

## Objetivo
Esta API permite testar, pela interface do Swagger, os endpoints exigidos na especificação do trabalho de Programação Mobile.

## Como abrir o Swagger
1. Ative o ambiente virtual, se necessário.
2. Inicie o servidor Django:
```powershell
python manage.py runserver
```
3. Abra no navegador:
```text
http://127.0.0.1:8000/api/docs/
```

## Teste do login
Abra a seção `POST /login`.
Clique em `Try it out` e envie este body:
```json
{
  "email": "usuario@esoft.com",
  "password": "Abc123"
}
```
Resultado esperado:
```json
{
  "token": "uuid-gerado"
}
```

## Teste de criação de jogo
Abra a seção `POST /jogos`.
Clique em `Try it out` e envie este body:
```json
{
  "nome": "Elden Ring",
  "tipo": "RPG",
  "nota": 6.5,
  "review": "Excelente jogo"
}
```
Resultado esperado:
- status `201 Created`
- retorno do objeto criado com `id`

Observação: no Swagger/JSON, valores decimais usam ponto, então `6.5` é válido e `6,5` não é um número JSON.

## Teste de listagem
Abra a seção `GET /jogos` e execute a requisição.
Resultado esperado:
- status `200 OK`
- lista com todos os jogos cadastrados

## Teste de busca por ID
Abra a seção `GET /jogos/{id}`.
Informe um ID existente, por exemplo `1`.
Resultado esperado:
- status `200 OK`
- retorno do jogo correspondente

## Teste de atualização
Abra a seção `PUT /jogos/{id}`.
Informe um ID existente e envie este body:
```json
{
  "nome": "Elden Ring DLC",
  "tipo": "RPG",
  "nota": 9.5,
  "review": "Muito bom"
}
```
Resultado esperado:
- status `200 OK`
- retorno do objeto atualizado

Observação: no Swagger/JSON, valores decimais usam ponto.

## Teste de remoção
Abra a seção `DELETE /jogos/{id}`.
Informe um ID existente e execute.
Resultado esperado:
- status `204 No Content`
- sem corpo de resposta

## Observações
- O Swagger está disponível em `http://127.0.0.1:8000/api/docs/`.
- O login do trabalho usa credenciais fixas da especificação.
- Os endpoints de jogos seguem o CRUD pedido no PDF.

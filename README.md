# JWT Validator API

API desenvolvida em Python para validar tokens JWT de acordo com as regras definidas no backend-challenge.

A aplicação recebe um JWT como string e informa, por meio de um booleano, se o token possui uma estrutura aceitável e se seu payload atende às regras de negócio do desafio.

## Objetivo

A API deve validar se um token:

* possui estrutura JWT válida para o escopo da solução;
* contém exatamente as claims `Name`, `Role` e `Seed`;
* não contém claims adicionais;
* possui `Name` sem caracteres numéricos e com no máximo 256 caracteres;
* possui `Role` exatamente igual a `Admin`, `Member` ou `External`;
* possui `Seed` representando um número inteiro primo.

Tokens e valores malformados são tratados de maneira segura e não devem provocar erro interno da aplicação.

---

## Tecnologias

A solução utiliza:

* Python 3.11 ou superior;
* FastAPI;
* Pydantic;
* PyJWT;
* Uvicorn;
* pytest;
* HTTPX / FastAPI TestClient;
* pytest-cov;
* Ruff.

# Arquitetura

A aplicação foi organizada com separação entre protocolo HTTP, contratos, coordenação da validação e regras de negócio.

```text
jwt-validator-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── jwt_routes.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── jwt_schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── jwt_validation_service.py
│   └── validators/
│       ├── __init__.py
│       ├── claim_validators.py
│       └── prime_validator.py
├── tests/
│   ├── conftest.py
│   ├── integration/
│   │   ├── test_health.py
│   │   └── test_jwt_routes.py
│   └── unit/
│       ├── test_claim_validators.py
│       ├── test_jwt_validation_service.py
│       └── test_prime_validator.py
├── .gitignore
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
└── README.md
```

## Responsabilidade das camadas

### `app/main.py`

Cria e configura a aplicação FastAPI e registra os routers.

Também disponibiliza o endpoint de health check.

### `app/api/`

Contém as responsabilidades relacionadas ao protocolo HTTP.

A rota recebe a requisição, chama o serviço de validação e constrói a resposta.

Nenhuma regra de `Name`, `Role`, `Seed` ou primalidade fica nessa camada.

### `app/schemas/`

Contém os modelos Pydantic que representam os contratos da API.

### `app/services/`

Coordena o fluxo de validação do JWT.

O serviço:

1. recebe o token;
2. verifica sua estrutura;
3. tenta decodificar header e payload;
4. trata erros esperados de JWT;
5. envia o payload para os validadores;
6. retorna `True` ou `False`.

### `app/validators/`

Contém regras independentes de negócio.

São responsáveis por:

* quantidade e nome das claims;
* validação de `Name`;
* validação de `Role`;
* conversão e validação de `Seed`;
* verificação de números primos.

### `tests/unit/`

Testa regras e serviços isoladamente, sem depender de HTTP.

### `tests/integration/`

Realiza requisições à aplicação em memória e verifica a integração entre FastAPI, Pydantic, rota, serviço e validadores.

---

# Decisões de arquitetura

A solução prioriza:

* baixo acoplamento;
* alta coesão;
* funções pequenas;
* responsabilidades claras;
* tipagem;
* facilidade de teste;
* simplicidade.

Não foram introduzidas interfaces, factories, repositories ou classes abstratas apenas para demonstrar padrões arquiteturais.

O projeto é pequeno e não possui múltiplas implementações de serviços ou dependências externas que justifiquem essas abstrações.

Princípios SOLID aparecem principalmente pela separação de responsabilidades.

Por exemplo:

```text
HTTP
 ↓
Rota
 ↓
Serviço
 ↓
Validadores
```

A camada de validação não depende do FastAPI, permitindo que suas regras sejam testadas diretamente.

---

# Pré-requisitos

* Python 3.11 ou superior;
* Git.

Para verificar a versão instalada:

```bash
python --version
```

No Windows também pode ser utilizado:

```powershell
py --version
```

---

# Instalação

Clone o repositório:

```bash
git clone https://github.com/tatiane-ss/backend-challenge-tssgaec.git
```

Entre na pasta:

```bash
cd backend-challenge
```

## Criar o ambiente virtual

### Windows PowerShell

```powershell
py -m venv .venv
```

Caso `py` não esteja disponível:

```powershell
python -m venv .venv
```

---

# Ativar o ambiente virtual

## Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# Instalar as dependências

Para instalar somente as dependências necessárias para executar a aplicação:

```bash
python -m pip install -r requirements.txt
```

Para ambiente de desenvolvimento, incluindo testes, cobertura e lint:

```bash
python -m pip install -r requirements-dev.txt
```

O `requirements-dev.txt` também instala as dependências presentes em `requirements.txt`.

---

# Executar a aplicação

Na raiz do projeto:

```bash
python -m uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000
```

O argumento `--reload` é utilizado durante desenvolvimento para reiniciar automaticamente o servidor quando arquivos são alterados.

---

# Health check

Para verificar se a aplicação está funcionando:

```http
GET /health
```

Resposta:

```json
{
  "status": "ok"
}
```

---

# Documentação automática

Com a aplicação em execução, a documentação interativa pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

O documento OpenAPI pode ser consultado em:

```text
http://127.0.0.1:8000/openapi.json
```

---

# Endpoint de validação

## Requisição

```http
POST /api/v1/jwt/validate
Content-Type: application/json
```

Body:

```json
{
  "token": "JWT_AQUI"
}
```

---

## Token válido

Status:

```http
200 OK
```

Resposta:

```json
{
  "valid": true
}
```

---

## Token inválido

Status:

```http
200 OK
```

Resposta:

```json
{
  "valid": false
}
```

Um JWT inválido é tratado como resultado normal da operação.

O HTTP 200 indica que a API conseguiu executar a validação. O booleano indica o resultado dessa operação.

---

# Erros de contrato HTTP

Uma requisição que não respeite o contrato da API é diferente de um JWT que simplesmente não passa nas regras de validação.

Por exemplo:

```json
{}
```

ou:

```json
{
  "token": null
}
```

ou:

```json
{
  "token": 123
}
```

resultam em:

```http
422 Unprocessable Entity
```

O campo `token` utiliza validação estrita de string.

Campos adicionais no body da requisição também são rejeitados.

---

# Regras de validação

## Estrutura JWT

Antes das regras de negócio, a aplicação verifica se:

* a entrada é uma string;
* a string não está vazia;
* existem exatamente três segmentos;
* os segmentos não estão vazios;
* os segmentos utilizam caracteres aceitos pela representação Base64URL utilizada pelo projeto;
* o header pode ser interpretado como objeto JSON;
* o payload pode ser interpretado como objeto JSON.

A estrutura esperada é:

```text
HEADER.PAYLOAD.SIGNATURE
```

Um token estruturalmente inválido retorna:

```json
{
  "valid": false
}
```

sem gerar erro HTTP 500.

---

# Claims

O payload deve possuir exatamente:

```text
Name
Role
Seed
```

A validação compara o conjunto de chaves recebido com o conjunto esperado.

Isso rejeita tanto claims ausentes quanto claims adicionais.

Por exemplo, este payload é inválido:

```json
{
  "Name": "Maria",
  "Role": "Admin",
  "Seed": "7",
  "Org": "BR"
}
```

Os nomes são sensíveis a letras maiúsculas e minúsculas.

Portanto:

```text
Name
```

é diferente de:

```text
name
```

---

# Regra de Name

`Name` deve:

* ser uma string;
* possuir conteúdo;
* possuir no máximo 256 caracteres;
* não conter caracteres classificados como dígitos.

São aceitos, por exemplo:

```text
Maria Oliveira
João da Silva
Ana-Clara
D'Ávila
```

Espaços, acentos, hífens e apóstrofos não são proibidos pelo desafio e, portanto, não foram bloqueados pela solução.

Nomes vazios ou compostos apenas por espaços são rejeitados como premissa da aplicação.

Para detectar dígitos é utilizado `str.isdigit()`.

A solução não utiliza uma expressão limitada a `[0-9]`, permitindo que a intenção da regra também seja aplicada a caracteres Unicode classificados como dígitos.

---

# Regra de Role

`Role` deve ser uma string exatamente igual a:

```text
Admin
Member
External
```

A comparação é sensível a maiúsculas e minúsculas.

Assim:

```text
Admin
```

é válido, enquanto:

```text
admin
Admin 
 Admin
```

são inválidos.

A aplicação não normaliza valores silenciosamente com `lower()`, `strip()` ou transformações semelhantes.

---

# Regra de Seed

`Seed` deve representar um número inteiro primo.

A solução aceita:

```json
{
  "Seed": 7841
}
```

e:

```json
{
  "Seed": "7841"
}
```

Strings numéricas são aceitas porque as próprias massas do desafio apresentam `Seed` dessa forma.

Uma Seed textual deve possuir apenas dígitos ASCII.

São rejeitados:

```text
""
"sete"
"7.0"
"-7"
"+7"
" 7 "
```

Também são rejeitados:

* valores booleanos;
* números de ponto flutuante;
* valores nulos;
* números negativos;
* zero;
* um.

Zeros à esquerda são aceitos:

```text
"0007"
```

e o valor é interpretado como:

```text
7
```

---

# Verificação de número primo

Um número primo é um inteiro maior que 1 que possui exatamente dois divisores positivos: `1` e ele próprio.

Por isso:

```text
0 → não primo
1 → não primo
2 → primo
```

O algoritmo:

1. rejeita valores menores que 2;
2. aceita 2;
3. rejeita os demais números pares;
4. testa apenas divisores ímpares;
5. encerra quando o quadrado do divisor ultrapassa o número.

Não é necessário testar divisores maiores que a raiz quadrada, pois um divisor maior teria um divisor correspondente menor que ela.

A complexidade aproximada é:

```text
O(√n)
```

Essa estratégia é suficiente para os valores apresentados pelo desafio.

---

# Tratamento da assinatura do JWT

Esta é a principal premissa técnica da solução.

Um JWT normalmente possui:

```text
header.payload.signature
```

Header e payload utilizam uma codificação que pode ser decodificada sem conhecer uma senha.

Decodificar esses dados não significa comprovar sua autenticidade.

## Limitação do enunciado

O desafio fornece JWTs assinados, mas não fornece:

* chave secreta;
* chave pública;
* JWKS;
* URL de um emissor;
* algoritmo permitido definido pela aplicação.

Por esse motivo, não é tecnicamente possível confirmar criptograficamente a assinatura dos tokens fornecidos.

A solução utiliza PyJWT com a verificação da assinatura explicitamente desabilitada para conseguir interpretar a estrutura e aplicar as regras do desafio.

Portanto:

```text
token estruturalmente válido
+
claims válidas
```

não significa:

```text
assinatura criptograficamente autenticada
```

A resposta `valid: true` significa que o token possui estrutura aceitável para o escopo do desafio e que seu payload atende às regras de negócio implementadas.

---

# Como a assinatura seria validada futuramente

Caso uma chave secreta apropriada fosse fornecida para tokens HS256, a validação poderia utilizar uma configuração equivalente a:

```python
jwt.decode(
    token,
    key=secret,
    algorithms=["HS256"],
)
```

A lista de algoritmos permitidos deve ser definida pela aplicação.

Ela não deve ser construída dinamicamente apenas a partir do valor `alg` recebido no próprio token.

Por exemplo, a aplicação não deverá utilizar o algoritmo informado por uma entrada não confiável para decidir sozinha quais algoritmos aceitar.

Em uma solução com algoritmos assimétricos, uma chave pública ou mecanismo como JWKS poderia ser utilizado.

---

# Premissas adotadas

Como alguns detalhes não estão explicitamente definidos no desafio, foram adotadas as seguintes premissas:

1. “JWT válido” significa, para este case, estrutura JWT interpretável mais cumprimento das regras de negócio, sem afirmação de autenticidade criptográfica.

2. O token deve possuir três segmentos não vazios.

3. `Seed` pode ser inteiro JSON ou string decimal, pois as massas fornecidas utilizam strings.

4. Valores booleanos não são aceitos como Seed.

5. Números decimais não são aceitos como Seed, mesmo quando representados como `7.0`.

6. Strings de Seed não são normalizadas antes da validação.

7. Zeros à esquerda são permitidos.

8. `Name` vazio ou contendo apenas espaços é considerado inválido.

9. Espaços internos, acentos, hífens e apóstrofos são permitidos em `Name`.

10. `Role` é comparada de maneira exata e case-sensitive.

11. Campos adicionais no body HTTP são rejeitados.

12. Claims adicionais no payload JWT tornam o token inválido.

---

# Testes

O projeto utiliza pytest e possui testes unitários e de integração.

## Testes unitários

Os testes unitários verificam as regras sem depender do FastAPI.

São cobertos cenários como:

### Name

* nome comum;
* nome com espaços;
* nome com acento;
* nome com hífen;
* nome com apóstrofo;
* nome contendo número;
* nome vazio;
* apenas espaços;
* exatamente 256 caracteres;
* 257 caracteres;
* tipo incorreto;
* valor nulo.

### Role

* `Admin`;
* `Member`;
* `External`;
* valor desconhecido;
* caixa incorreta;
* espaços adicionais;
* valor vazio;
* valor nulo;
* tipo incorreto.

### Seed

* números primos;
* número primo representado como string;
* zeros à esquerda;
* números compostos;
* zero;
* um;
* negativos;
* valores decimais;
* string não numérica;
* string vazia;
* booleanos;
* nulo;
* números presentes nas massas do desafio.

### JWT e claims

* exatamente três claims;
* claim ausente;
* claim adicional;
* diferença de maiúsculas e minúsculas;
* estrutura JWT inválida;
* segmentos vazios;
* JSON inválido;
* payload que não seja objeto JSON;
* quatro massas oficiais do desafio.

---

# Testes de integração

Os testes de integração utilizam o TestClient do FastAPI.

Não é necessário iniciar o Uvicorn para executá-los.

O fluxo exercitado é:

```text
requisição
   ↓
FastAPI
   ↓
Pydantic
   ↓
rota
   ↓
serviço
   ↓
validadores
   ↓
resposta
```

São verificados:

* token válido;
* JWT estruturalmente inválido;
* `Name` contendo número;
* claim adicional;
* claim ausente;
* `Role` inválida;
* `Seed` não prima;
* token vazio;
* body ausente;
* campo `token` ausente;
* tipos incorretos;
* campos HTTP adicionais;
* ausência de HTTP 500 para entradas inválidas conhecidas.

---

# Executar os testes

Toda a suíte:

```bash
pytest -v
```

Somente testes unitários:

```bash
pytest tests/unit -v
```

Somente testes de integração:

```bash
pytest tests/integration -v
```

---

# Qualidade de código

As configurações estão centralizadas em:

```text
pyproject.toml
```

## Lint

```bash
ruff check .
```

## Verificar formatação

```bash
ruff format --check .
```

## Formatar

```bash
ruff format .
```

---

# Cobertura

Para executar testes e visualizar cobertura:

```bash
pytest --cov=app --cov-report=term-missing
```

A cobertura é utilizada como ferramenta para encontrar comportamentos relevantes ainda não exercitados pelos testes.

---

# Decisões relacionadas a SOLID

SOLID foi utilizado como conjunto de princípios de design e não como uma checklist para criação artificial de classes.

O princípio mais visível na solução é o de responsabilidade única:

```text
rota
→ HTTP

schema
→ contratos

serviço
→ coordenação da validação

validadores
→ regras de negócio
```

A separação também reduz o acoplamento entre infraestrutura e domínio.

Princípios relacionados a interfaces e substituição não exigiram implementação explícita porque o projeto não possui hierarquias de classes ou múltiplas implementações que justifiquem essas abstrações.

---

# Segurança

Algumas decisões de segurança adotadas:

* JWT inválido é tratado sem provocar erro 500 esperado;
* exceções específicas do PyJWT são tratadas;
* não é utilizado `except Exception` indiscriminadamente;
* o JWT completo não deve ser registrado em logs;
* a assinatura não é apresentada como validada sem uma chave;
* o algoritmo informado pelo token não deve determinar sozinho os algoritmos aceitos pela aplicação;
* valores inválidos não são silenciosamente normalizados para se tornarem válidos.

---

# Limitações

## Assinatura não autenticada

A principal limitação é a ausência de validação criptográfica da assinatura devido à falta da chave necessária no enunciado.

## Números extremamente grandes

A primalidade utiliza um algoritmo `O(√n)`.

Ele é adequado para os valores do desafio, mas pode se tornar caro para números extremamente grandes.

O case não define um limite máximo para `Seed`, então nenhum limite arbitrário foi introduzido.

## Chaves JSON duplicadas

A solução utiliza o comportamento padrão de decodificação JSON da biblioteca utilizada.

Um caso extremo de JSON contendo chaves duplicadas não recebe tratamento específico nesta versão.

## Motivos de invalidação

A API retorna apenas:

```json
{
  "valid": false
}
```

Ela não informa ao consumidor qual regra falhou.

Essa decisão mantém o contrato próximo ao requisito original, que solicita essencialmente um booleano.

---

# Possíveis melhorias futuras

Em uma evolução para produção poderiam ser consideradas:

* validação criptográfica da assinatura;
* configuração segura das chaves;
* lista explícita de algoritmos permitidos;
* validação de emissor (`iss`);
* validação de audiência (`aud`);
* validação de expiração (`exp`), caso essas claims passem a fazer parte do contrato;
* obtenção de chaves via JWKS para algoritmos assimétricos;
* limite explícito de tamanho do token;
* limite explícito para tamanho de `Seed`;
* algoritmo de primalidade apropriado para números muito grandes;
* tratamento específico de JSON com chaves duplicadas;
* logs estruturados sem exposição do token;
* observabilidade e métricas;
* análise estática de tipos com Mypy caso o projeto cresça;
* CI para execução automática de lint e testes.

Docker, scripts de CI/CD, coleções de Postman e publicação em cloud não foram adicionados porque não fazem parte dos pontos exigidos para esta entrega.

---

# Resumo do fluxo

```text
POST /api/v1/jwt/validate
          ↓
validação do contrato HTTP
          ↓
validação estrutural do JWT
          ↓
decodificação do payload
          ↓
exatamente Name, Role e Seed?
          ↓
Name válido?
          ↓
Role válida?
          ↓
Seed inteira e prima?
          ↓
{"valid": true}
```

Qualquer falha nas regras de JWT ou negócio resulta em:

```json
{
  "valid": false
}
```

Entradas que não respeitam o contrato HTTP são rejeitadas antes desse fluxo com HTTP 422.

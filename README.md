# Prática Avaliada 2

Avaliação prática com 4 exercícios cobrindo APIs RESTful, banco de dados, testes e segurança com JWT. Total: **10 pontos**.

---

## Exercício 1 — API RESTful com C# e ASP.NET Core (2,5 pts)

Criação de uma API simples para gerenciar produtos.

### O que implementar

- **Controller** com 3 endpoints:
  - `POST` — recebe um produto no corpo da requisição (`[FromBody]`)
  - `GET/{id}` — retorna o produto ou `404 Not Found`
  - `GET` — retorna todos os produtos com `200 OK`

- **Validação com Data Annotations** nos campos:
  - `Nome` — `[Required]` e `[StringLength]`
  - `Preco` — `[Required]` e `[Range]`

- **Códigos HTTP esperados:**
  - `201 Created` — produto criado com sucesso
  - `200 OK` — listagem/busca bem-sucedida
  - `400 Bad Request` — dados inválidos

### Critérios de avaliação

| Critério | Pontos |
|---|---|
| Controller estruturado corretamente | 1,0 |
| Endpoints funcionais | 0,6 |
| Validação com Data Annotations | 0,5 |
| Códigos de status HTTP corretos | 0,4 |

---

## Exercício 2 — Persistência com SQLAlchemy (2,5 pts)

Configuração do ORM SQLAlchemy para salvar produtos em banco de dados SQLite.

### O que implementar

- **Configurar** engine e criar as tabelas com `Base.metadata.create_all(bind=engine)`

- **Modelo `Product`** com:
  - `__tablename__ = "products"`
  - Campos tipados com `Mapped[tipo]` e `mapped_column`

- **Operações CRUD:**
  - `create_product`
  - `read_all_products`
  - `update_product_price`
  - `delete_product`

### Critérios de avaliação

| Critério | Pontos |
|---|---|
| Configuração do SQLAlchemy | 0,6 |
| Modelo definido corretamente | 1,0 |
| Operações CRUD implementadas | 0,5 |
| Gerenciamento de sessão | 0,4 |

---

## Exercício 3 — Testes de API com pytest (3,0 pts)

Testes automatizados para uma API FastAPI usando `pytest` e `TestClient`.

### O que implementar

- **Testar o endpoint POST** com dados válidos e inválidos (usar `assert`)
- **Testar o endpoint GET** com ID existente e inexistente (verificar `status_code`)
- **Usar fixtures** para preparar os dados de teste com `@pytest.fixture`

### Critérios de avaliação

| Critério | Pontos |
|---|---|
| Configuração dos testes | 1,0 |
| Teste de criação de produto | 1,0 |
| Teste de validação | 0,5 |
| Cenários positivo e negativo | 0,5 |

---

## Exercício 4 — Segurança com JWT (2,0 pts)

Autenticação com JSON Web Token para proteger endpoints da API.

### O que implementar

- **Endpoint de login** que retorna um token JWT válido
- **Middleware de validação JWT** para verificar o token nas requisições
- **Hash de senhas** antes de armazenar/comparar
- **Proteger o endpoint de criação de produtos** (requer token válido)

### Critérios de avaliação

| Critério | Pontos |
|---|---|
| Endpoint de login | 0,6 |
| Geração e validação do JWT | 0,6 |
| Hash de senhas | 0,4 |
| Proteção de endpoints | 0,4 |

---

## Uso de IA

Durante o desenvolvimento desta prática, utilizei o Claude (Anthropic) como ferramenta de apoio em três momentos distintos.

O primeiro foi para entender o funcionamento do `@pytest.fixture` e do `assert` no contexto do Exercício 3. Tinha dúvidas sobre como o decorator `@pytest.fixture` prepara e injeta dados de teste automaticamente nas funções de teste, e como o `assert` valida na prática o `status_code` e o corpo da resposta retornados pelo `TestClient` do FastAPI. A IA trouxe um pouco a mais a lógica por trás dessas estruturas com exemplos simples, o que me ajudou a entender o fluxo antes de escrever o código.

O segundo momento foi para entender como visualizar e testar as requisições no Postman. Consultei a IA para saber como configurar uma requisição `POST` com corpo JSON, como passar um token JWT no header `Authorization: Bearer <token>` para testar o Exercício 4, e como interpretar os códigos de status retornados (`201`, `200`, `400`, `404`). Me poupando tempo na configuração inicial do ambiente de testes manual.

O terceiro uso foi para a criação deste próprio README. Descrevi o conteúdo do enunciado e pedi ajuda para organizar as informações de forma clara, com tabelas de pontuação e seções separadas por exercício. O texto foi revisado e adaptado por mim para refletir meu entendimento real das tarefas.

Em todos os casos, verifiquei as informações fornecidas pela IA consultando a documentações e materiais de estudo antes de aplicá-las.

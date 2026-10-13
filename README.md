# Sistema de Gestão de Eventos

API REST desenvolvida com Django e Django REST Framework para gerenciar eventos, participantes e inscrições.

## Funcionalidades

- Cadastro, consulta, atualização e exclusão de eventos.
- Cadastro, consulta, atualização e exclusão de participantes.
- Gerenciamento de inscrições em eventos.
- Relacionamentos entre organizadores, eventos, participantes e inscrições.
- Atualização automática das vagas disponíveis por meio de Signals do Django.
- Autenticação JWT para proteger endpoints.
- Relatório de eventos com contagem de inscrições ativas.
- Testes automatizados para validar o funcionamento dos Signals.

## Tecnologias utilizadas

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite (banco de dados padrão do projeto)

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/dudavieiraoliveira/gestao_eventos_tb.git
cd gestao_eventos_tb
```

### 2. Criar e ativar o ambiente virtual

No Windows, usando PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt```

### 4. Executar as migrações

```bash
python manage.py migrate
```

### 5. Criar um superusuário

```bash
python manage.py createsuperuser
```

### 6. Iniciar o servidor

```bash
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/`.

## Endpoints principais

| Método | Endpoint | Descrição |
|---|---|---|
| GET, POST | `/api/eventos/` | Listar e cadastrar eventos |
| GET, PUT, PATCH, DELETE | `/api/eventos/{id}/` | Consultar, atualizar e excluir evento |
| GET, POST | `/api/participantes/` | Listar e cadastrar participantes |
| GET, PUT, PATCH, DELETE | `/api/participantes/{id}/` | Consultar, atualizar e excluir participante |
| GET, POST | `/api/inscricoes/` | Listar e cadastrar inscrições |
| GET, PUT, PATCH, DELETE | `/api/inscricoes/{id}/` | Consultar, atualizar e excluir inscrição |
| POST | `/api/token/` | Obter tokens JWT |
| POST | `/api/token/refresh/` | Renovar token de acesso |
| GET | `/api/relatorios/eventos/` | Consultar eventos e contar inscrições ativas |

O endpoint de eventos e o relatório exigem autenticação. Para acessá-los, envie o token de acesso no cabeçalho:

```http
Authorization: Bearer SEU_TOKEN_DE_ACESSO
```
## Autenticação JWT

A API utiliza autenticação JWT (JSON Web Token) para controlar o acesso aos endpoints protegidos. Para acessar esses recursos, é necessário obter um token de acesso e enviá-lo nas requisições.

### 1. Obter tokens

**Endpoint:** `POST /api/token/`

Envie uma requisição com o nome de usuário e a senha de um usuário cadastrado no Django:

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

A resposta contém dois tokens:

- `access`: token de acesso utilizado nas requisições autenticadas.
- `refresh`: token utilizado para renovar o token de acesso.

### 2. Acessar endpoints protegidos

Inclua o token de acesso no cabeçalho HTTP da requisição:

```http
Authorization: Bearer SEU_TOKEN_DE_ACESSO
```

O endpoint de eventos (`/api/eventos/`) e o relatório (`/api/relatorios/eventos/`) exigem autenticação.

### 3. Renovar o token de acesso

**Endpoint:** `POST /api/token/refresh/`

Envie o token de renovação:

```json
{
  "refresh": "SEU_TOKEN_DE_RENOVACAO"
}
```

A resposta fornece um novo token de acesso, que deve ser utilizado nas próximas requisições.

### 4. Testar a autenticação

É possível testar os endpoints utilizando a interface navegável da API do Django REST Framework ou uma ferramenta como Postman.

- Sem um token válido, os endpoints protegidos negam o acesso.
- Com um token de acesso válido, é possível realizar as operações autorizadas.

## Testes automatizados

Para executar os testes do aplicativo `eventos`:

```bash
python manage.py test eventos
```

Os testes verificam o comportamento das vagas disponíveis ao criar, cancelar e reativar inscrições, além da validação de inscrições quando não há vagas.

## Consultas avançadas

O relatório utiliza `annotate()`, `Count()` e o relacionamento reverso `related_name='inscricoes'` para contar as inscrições ativas de cada evento.

## Autor

Projeto acadêmico desenvolvido como prática de Django e construção de APIs REST.
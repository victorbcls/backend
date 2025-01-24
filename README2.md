# README

## Descrição do Projeto

Este projeto é uma API simples para gerenciar um catálogo de filmes, utilizando FastAPI e SQLAlchemy. A API permite realizar operações básicas como criar, listar, atualizar e excluir filmes. Os dados são armazenados em um banco de dados SQLite.

## Estrutura do Projeto

O projeto é organizado da seguinte forma:

- **app/**: Contém todos os arquivos da aplicação.
  - **main.py**: O ponto de entrada da aplicação, onde as rotas da API são definidas.
  - **crud.py**: Contém as funções que interagem com o banco de dados.
  - **schemas.py**: Define os modelos de dados utilizados pela API.
  - **models.py**: Define a estrutura do banco de dados.
  - **db.py**: Configurações do banco de dados.
  - \***\*init**.py\*\*: Inicializa o pacote.

## Funcionalidades

### 1. Listar Filmes

- **GET /filmes**: Retorna uma lista de todos os filmes ativos.
- **GET /filmes/inativos**: Retorna uma lista de todos os filmes inativos.

### 2. Criar Filme

- **POST /filmes**: Cria um novo filme. O corpo da requisição deve conter os dados do filme (título, diretor, ano e ativo). Se um filme com o mesmo título e ano já existir, um erro será retornado.

### 3. Obter Filme por ID

- **GET /filmes/{id}**: Retorna os detalhes de um filme específico, identificado pelo seu ID. Se o filme não for encontrado, um erro 404 será retornado.

### 4. Atualizar Filme

- **PUT /filmes/{id}**: Atualiza os dados de um filme existente. O corpo da requisição deve conter os novos dados do filme. Se o filme não for encontrado, um erro 404 será retornado.

### 5. Excluir Filme

- **DELETE /filmes/{id}**: Inativa um filme existente. Em vez de remover o filme do banco de dados, ele é marcado como inativo. Isso é feito para manter um histórico de filmes, permitindo que você recupere informações sobre filmes que não estão mais ativos, se necessário. Essa abordagem é útil para evitar a perda de dados e para manter a integridade referencial em sistemas que podem ter relacionamentos com outros dados.

## Como Funciona a Exclusão

A exclusão de um filme é realizada através da rota **DELETE /filmes/{id}**. Quando essa rota é chamada, a API verifica se o filme existe. Se existir, o filme é marcado como inativo, alterando o campo `ativo` para `False`. Isso significa que o filme não será mais exibido nas listas de filmes ativos, mas ainda estará presente no banco de dados.

Essa abordagem de "inativação" em vez de exclusão física é vantajosa por várias razões:

- **Histórico**: Permite manter um registro de todos os filmes, mesmo aqueles que não estão mais ativos.
- **Integridade dos Dados**: Evita problemas de integridade referencial que podem ocorrer se outros dados dependem do filme que está sendo excluído.
- **Recuperação**: Facilita a recuperação de informações sobre filmes que foram inativados, caso seja necessário.

## Como Executar o Projeto

### Usando Python Local

1. **Instalação das Dependências**: Certifique-se de ter o Python e o pip instalados. Em seguida, instale as dependências necessárias:

   ```bash
   pip install fastapi[all] sqlalchemy
   ```

2. **Executar a Aplicação**: Navegue até o diretório app e execute o seguinte comando:

   ```bash
   uvicorn main:app --reload
   ```

3. **Acessar a API**: A API estará disponível em `http://127.0.0.1:8000`. Você pode usar ferramentas como Postman ou Insomnia para testar as rotas, ou acessar a documentação automática gerada pelo FastAPI em `http://127.0.0.1:8000/docs`.

### Usando Docker Compose

1. **Pré-requisitos**: Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

2. **Executar o Container**: No diretório App do projeto, execute:

   ```bash
   docker-compose up --build
   ```

   Este comando irá:

   - Construir a imagem do container
   - Iniciar o serviço da API
   - Mapear a porta 8000 do container para a porta 8000 do seu host

3. **Acessar a API**: A API estará disponível em `http://localhost:8000`. A documentação pode ser acessada em `http://localhost:8000/docs`.

4. **Parar o Container**: Para parar a execução, use:

   ```bash
   docker-compose down
   ```

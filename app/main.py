# Importações necessárias
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import SessionLocal, Base, engine
from models import Filme
from schemas import FilmeBase, FilmeResponse
from crud import (
    get_filmes,
    create_filme,
    get_filme_by_id,
    update_filme,
    delete_filme,
    get_filmes_inativos,
)


# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
# Inicializa a aplicação FastAPI
app = FastAPI()


# Função para gerenciar a conexão com o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        # Garante que a conexão seja fechada mesmo se ocorrer erro
        db.close()


# Rota GET para listar todos os filmes
@app.get("/filmes", response_model=list[FilmeResponse], status_code=200)
def listar_filmes(db: Session = Depends(get_db)):
    try:
        filmes = get_filmes(db)
        for filme in filmes:
            filme.status = 200
        return filmes
    except SQLAlchemyError:
        # Retorna erro 500 se houver problema no banco
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados")


# Rota GET para listar filmes inativos
@app.get("/filmes/inativos", response_model=list[FilmeResponse], status_code=200)
def listar_filmes_inativos(db: Session = Depends(get_db)):
    try:
        filmes = get_filmes_inativos(db)
        for filme in filmes:
            filme.status = 200
        return filmes
    except SQLAlchemyError:
        # Retorna erro 500 se houver problema no banco
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados")


# Rota POST para criar um novo filme
@app.post("/filmes", response_model=FilmeResponse, status_code=201)
def criar_filme(filme: FilmeBase, db: Session = Depends(get_db)):
    try:
        filme_criado = create_filme(db, filme)
        filme_criado.status = 201
        return filme_criado
    except IntegrityError:
        # Erro 400 se tentar criar filme duplicado
        raise HTTPException(status_code=400, detail="Filme já existe no banco de dados")
    except SQLAlchemyError:
        # Erro 500 para outros problemas no banco
        raise HTTPException(
            status_code=500, detail="Erro ao criar filme no banco de dados"
        )


# Rota GET para buscar um filme específico pelo ID
@app.get("/filmes/{id}", response_model=FilmeResponse, status_code=200)
def obter_filme(id: int, db: Session = Depends(get_db)):
    try:
        filme = get_filme_by_id(db, id)
        if not filme:
            # Erro 404 se o filme não for encontrado
            raise HTTPException(status_code=404, detail="Filme não encontrado")
        filme.status = 200
        return filme
    except SQLAlchemyError:
        # Erro 500 para problemas no banco
        raise HTTPException(
            status_code=500, detail="Erro ao buscar filme no banco de dados"
        )


# Rota PUT para atualizar um filme existente
@app.put("/filmes/{id}", response_model=FilmeResponse, status_code=200)
def editar_filme(id: int, filme: FilmeBase, db: Session = Depends(get_db)):
    try:
        filme_data = filme.model_dump()
        filme_data["ativo"] = True  # Mantém o filme como ativo na atualização
        atualizado = update_filme(db, id, filme_data)
        if not atualizado:
            # Erro 404 se o filme não existir
            raise HTTPException(status_code=404, detail="Filme não encontrado")
        atualizado.status = 200
        return atualizado
    except IntegrityError:
        # Erro 400 se os dados forem inválidos
        raise HTTPException(status_code=400, detail="Dados inválidos para atualização")
    except SQLAlchemyError:
        # Erro 500 para problemas no banco
        raise HTTPException(
            status_code=500, detail="Erro ao atualizar filme no banco de dados"
        )


# Rota DELETE para remover um filme
@app.delete("/filmes/{id}", response_model=FilmeResponse, status_code=200)
def excluir_filme(id: int, db: Session = Depends(get_db)):
    try:
        excluido = delete_filme(db, id)
        if not excluido:
            # Erro 404 se o filme não existir
            raise HTTPException(status_code=404, detail="Filme não encontrado")
        excluido.status = 200
        return excluido
    except SQLAlchemyError:
        # Erro 500 para problemas no banco
        raise HTTPException(
            status_code=500, detail="Erro ao excluir filme do banco de dados"
        )

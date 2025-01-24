# Importações necessárias do SQLAlchemy e dos modelos/schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import Filme
from schemas import FilmeResponse


# Função para buscar todos os filmes ativos do banco de dados
def get_filmes(db: Session):
    try:
        # Faz a query para buscar filmes ativos ou inativos
        query = db.query(Filme).filter(Filme.ativo == True)
        filmes = query.all()
        # Converte cada filme do banco para o formato de resposta da API
        return [
            FilmeResponse(
                id=filme.id,
                titulo=filme.titulo,
                diretor=filme.diretor,
                ano=filme.ano,
                ativo=filme.ativo,
                detail="Filme encontrado com sucesso",
                status=200,
            )
            for filme in filmes
        ]
    except SQLAlchemyError as e:
        # Em caso de erro, desfaz as alterações e relança a exceção
        db.rollback()
        filme_response = FilmeResponse(
            id=0,
            titulo="",
            diretor="",
            ano=0,
            ativo=False,
            detail=f"Erro ao buscar filmes: {str(e)}",
            status=500,
        )
        return filme_response


# Função para buscar todos os filmes inativos do banco de dados
def get_filmes_inativos(db: Session):
    try:
        # Faz a query para buscar filmes inativos
        query = db.query(Filme).filter(Filme.ativo == False)
        filmes = query.all()
        # Converte cada filme do banco para o formato de resposta da API
        return [
            FilmeResponse(
                id=filme.id,
                titulo=filme.titulo,
                diretor=filme.diretor,
                ano=filme.ano,
                ativo=filme.ativo,
                detail="Filme inativo encontrado com sucesso",
                status=200,
            )
            for filme in filmes
        ]
    except SQLAlchemyError as e:
        # Em caso de erro, desfaz as alterações e relança a exceção
        db.rollback()
        filme_response = FilmeResponse(
            id=0,
            titulo="",
            diretor="",
            ano=0,
            ativo=False,
            detail=f"Erro ao buscar filmes inativos: {str(e)}",
            status=500,
        )
        return filme_response


# Função para criar um novo filme no banco de dados
def create_filme(db: Session, filme: FilmeResponse):
    try:
        # Verifica se já existe um filme com mesmo título e ano
        filme_existente = (
            db.query(Filme)
            .filter(Filme.titulo == filme.titulo, Filme.ano == filme.ano)
            .first()
        )

        if filme_existente:
            filme_response = FilmeResponse(
                id=0,
                titulo="",
                diretor="",
                ano=0,
                ativo=False,
                detail="Filme já existe no banco de dados",
                status=400,
            )
            return filme_response

        # Cria uma nova instância do modelo Filme com os dados recebidos
        novo_filme = Filme(titulo=filme.titulo, diretor=filme.diretor, ano=filme.ano)
        # Adiciona o novo filme ao banco
        db.add(novo_filme)
        # Confirma as alterações
        db.commit()
        # Atualiza o objeto com os dados do banco
        db.refresh(novo_filme)
        # Retorna o filme criado no formato de resposta
        filme_response = FilmeResponse(
            id=novo_filme.id,
            titulo=novo_filme.titulo,
            diretor=novo_filme.diretor,
            ano=novo_filme.ano,
            detail="Filme criado com sucesso",
            ativo=True,
            status=201,
        )
        return filme_response
    except SQLAlchemyError as e:
        # Outros erros do banco de dados
        db.rollback()
        filme_response = FilmeResponse(
            id=0,
            titulo="",
            diretor="",
            ano=0,
            ativo=False,
            detail=f"Erro ao criar filme: {str(e)}",
            status=500,
        )
        return filme_response


# Função para buscar um filme específico pelo ID
def get_filme_by_id(
    db: Session,
    id: int,
):
    try:
        # Busca o filme pelo ID
        query = db.query(Filme).filter(Filme.id == id)

        filme = query.first()
        if filme:
            # Se encontrou, retorna no formato de resposta
            filme_response = FilmeResponse(
                id=filme.id,
                titulo=filme.titulo,
                diretor=filme.diretor,
                ano=filme.ano,
                detail="Filme encontrado com sucesso",
                ativo=filme.ativo,
                status=200,
            )
            return filme_response
        # Se não encontrou, retorna None
        return None
    except SQLAlchemyError as e:
        db.rollback()
        filme_response = FilmeResponse(
            id=0,
            titulo="",
            diretor="",
            ano=0,
            ativo=False,
            detail=f"Erro ao buscar filme por ID: {str(e)}",
            status=500,
        )
        return filme_response


# Função para atualizar um filme existente
def update_filme(db: Session, id: int, filme_data: dict):
    try:
        # Primeiro verifica se o filme existe e está ativo
        db_filme = get_filme_by_id(db, id)
        if not db_filme:
            return None

        # Acesse os dados do dicionário diretamente
        titulo = filme_data["titulo"]
        diretor = filme_data["diretor"]
        ano = filme_data["ano"]
        ativo = filme_data["ativo"]

        # Busca o filme e atualiza seus campos
        filme_obj = db.query(Filme).filter(Filme.id == id).first()
        filme_obj.titulo = titulo
        filme_obj.diretor = diretor
        filme_obj.ano = ano
        filme_obj.ativo = ativo

        # Confirma as alterações
        db.commit()
        db.refresh(filme_obj)
        # Retorna o filme atualizado
        filme_response = FilmeResponse(
            id=filme_obj.id,
            titulo=filme_obj.titulo,
            diretor=filme_obj.diretor,
            ano=filme_obj.ano,
            detail="Filme atualizado com sucesso",
            ativo=True,
            status=200,
        )
        return filme_response
    except IntegrityError:
        # Erro se os dados forem inválidos
        db.rollback()
        filme_response = FilmeResponse(
            id=0,
            titulo="",
            diretor="",
            ano=0,
            ativo=False,
            detail="Erro: Dados inválidos para atualização",
            status=400,
        )
        return filme_response
    except SQLAlchemyError as e:
        db.rollback()
        filme_response = FilmeResponse(
            id=0,
            titulo="",
            diretor="",
            ano=0,
            ativo=False,
            detail=f"Erro ao atualizar filme: {str(e)}",
            status=500,
        )
        return filme_response


# Função para inativar um filme do banco de dados
def delete_filme(db: Session, id: int):
    try:
        # Verifica se o filme existe e está ativo
        db_filme = get_filme_by_id(db, id)
        if not db_filme:
            return None

        # Busca e inativa o filme
        filme_obj = db.query(Filme).filter(Filme.id == id).first()
        filme_obj.ativo = False
        db.commit()
        db.refresh(filme_obj)
        # Retorna o filme que foi inativado
        filme_response = FilmeResponse(
            id=id,
            titulo=db_filme.titulo,
            diretor=db_filme.diretor,
            ano=db_filme.ano,
            detail="Filme inativado com sucesso",
            ativo=False,
            status=200,
        )
        return filme_response
    except SQLAlchemyError as e:
        db.rollback()
        filme_response = FilmeResponse(
            id=0,
            titulo="",
            diretor="",
            ano=0,
            ativo=False,
            detail=f"Erro ao inativar filme: {str(e)}",
            status=500,
        )
        return filme_response

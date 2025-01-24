from sqlalchemy import Column, Integer, String, Boolean
from db import Base


class Filme(Base):
    __tablename__ = "filmes"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    diretor = Column(String)
    ano = Column(Integer)
    ativo = Column(Boolean, default=True)

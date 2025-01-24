from pydantic import BaseModel


class FilmeBase(BaseModel):
    titulo: str
    diretor: str
    ano: int
    ativo: bool


class FilmeResponse(FilmeBase):
    id: int
    detail: str
    status: int

    class Config:
        from_attributes = True

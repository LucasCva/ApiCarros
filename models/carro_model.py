from typing import Optional

from pydantic import BaseModel



class CarroResponse(BaseModel):
    id: int
    nome: str
    ano: int
    modelo: str


class CarroRequest(BaseModel):
    nome: str
    ano: int
    modelo: str


class CarroUpdate(BaseModel):
    nome: Optional[str] = None
    ano: Optional[int] = None
    modelo: Optional[str] = None

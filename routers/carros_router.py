from typing import List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from pydantic import BaseModel
from sqlalchemy import Null
from sqlalchemy.orm import Session

from models.carro_model import Carros
from shared.dependencies import get_db

# instanciando o api router
router = APIRouter(prefix='/carros')


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
    nome: Optional[str] = Null
    ano: Optional[int] = Null
    modelo: Optional[str] = Null


# Create carro
@router.post('/', response_model=CarroResponse, status_code=201)
def criar_carro(carro_request: CarroRequest, db: Session = Depends(get_db)) -> CarroResponse:
    # carro = Carros(nome= carro.nome, ano=carro.ano, modelo=carro.modelo)
    carro = Carros(
        nome=carro_request.nome,
        ano=carro_request.ano,
        modelo=carro_request.modelo
    )
    db.add(carro)
    db.commit()
    db.refresh(carro)

    return CarroResponse(
        id=carro.id,
        nome=carro.nome,
        ano=carro.ano,
        modelo=carro.modelo
    )


# Listar carros
@router.get('/', response_model=List[CarroResponse])
def listar_carros(db: Session = Depends(get_db)) -> List[CarroResponse]:
    return db.query(Carros).all()


# Encontrar carro pelo ID

@router.get('/{id_carro}/', response_model=CarroResponse)
def encontrar_carro_pelo_id(id_carro: int = Path(..., ge=1), db: Session = Depends(get_db)) -> CarroResponse:
    carro = db.query(Carros).filter(Carros.id == id_carro).first()
    if not carro:
        raise HTTPException(status_code=404, detail='Carro não encontrado')

    return CarroResponse(
        id=carro.id,
        nome=carro.nome,
        ano=carro.ano,
        modelo=carro.modelo

    )


# Update carro
@router.put('/{id_carro}/')
def modificar_carro(
        carro_updade: CarroUpdate,
        id_carro: int = Path(..., ge=1),
        db: Session = Depends(get_db)) -> CarroResponse:
    carro = db.query(Carros).filter(Carros.id == id_carro).first()
    if not carro:
        raise HTTPException(status_code=404, detail='Carro não encontrado')

    for field, value in carro_updade.model_dump().items():
        if value is not None:
            setattr(carro, field, value)

    db.commit()
    db.refresh(carro)

    return CarroResponse(
        id=carro.id,
        nome=carro.nome,
        ano=carro.ano,
        modelo=carro.modelo
    )


# Delete carro
@router.delete('/{id_carro}/', status_code=204)
def deletar_carro_pelo_id(id_carro: int = Path(..., ge=1), db: Session = Depends(get_db)):
    carro = db.query(Carros).filter(Carros.id == id_carro).first()
    if not carro:
        raise HTTPException(status_code=404, detail='Carro não encontrado')
    db.delete(carro)
    db.commit()

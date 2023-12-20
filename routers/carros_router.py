from typing import List, Type

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path
from sqlalchemy.orm import Session

from database.models.carro_model import Carros
from models.carro_model import CarroResponse, CarroRequest, CarroUpdate
from shared.dependencies import get_db

# instanciando o api router
router = APIRouter(prefix='/carros')


# Create carro
@router.post('/', response_model=CarroResponse, status_code=201)
def criar_carro(carro_request: CarroRequest, db: Session = Depends(get_db)) -> CarroResponse:
    carro = Carros(**carro_request.model_dump())
    db.add(carro)
    db.commit()
    db.refresh(carro)
    return CarroResponse(**carro.__dict__)


# Listar carros
@router.get('/', response_model=List[CarroResponse])
def listar_carros(db: Session = Depends(get_db)) -> list[Type[Carros]]:
    return db.query(Carros).all()


# Encontrar carro pelo ID

@router.get('/{id_carro}/', response_model=CarroResponse)
def encontrar_carro_pelo_id(id_carro: int = Path(..., ge=1), db: Session = Depends(get_db)) -> CarroResponse:
    carro = db.query(Carros).filter(Carros.id == id_carro).first()
    if not carro:
        raise HTTPException(status_code=404, detail='Carro não encontrado')

    return CarroResponse(**carro.__dict__)


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

    return CarroResponse(**carro.__dict__)


# Delete carro
@router.delete('/{id_carro}/', status_code=204)
def deletar_carro_pelo_id(id_carro: int = Path(..., ge=1), db: Session = Depends(get_db)):
    carro = db.query(Carros).filter(Carros.id == id_carro).first()
    if not carro:
        raise HTTPException(status_code=404, detail='Carro não encontrado')
    db.delete(carro)
    db.commit()

import uvicorn
from fastapi import FastAPI

from routers import carros_router
from shared.database import Base, engine
from models.carro_model import Carros

app = FastAPI()

app.include_router(carros_router.router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)

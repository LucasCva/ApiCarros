import uvicorn
from fastapi import FastAPI

from routers import carros_router

app = FastAPI()

app.include_router(carros_router.router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)

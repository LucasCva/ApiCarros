from shared.database import SessionLocal


# Cria uma sessão local para o comunicação com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

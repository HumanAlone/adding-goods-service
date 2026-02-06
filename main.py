import uvicorn
from fastapi import FastAPI

from app.api import router
from app.database import Base, SessionLocal, engine
from app.models import Product
from sql.seed_data import seed_database

Base.metadata.create_all(bind=engine)

# Заполняем БД тестовыми данными
db = SessionLocal()
try:
    if db.query(Product).count() == 0:
        db.close()
        seed_database()
except Exception:
    pass
finally:
    db.close()

app = FastAPI(
    title="Сервис добавления товаров в заказ",
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

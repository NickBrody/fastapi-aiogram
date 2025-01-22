from contextlib import asynccontextmanager
from sqlalchemy.future import select
import uvicorn
import httpx
from fastapi import FastAPI, Depends
from models import Product
from schemas import ProductIn
from database import engine, Base, session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действия при старте приложения
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Переход к запуску приложения

    # Действия при остановке приложения
    await engine.dispose()

# Инициализация FastAPI с lifespan
app = FastAPI(lifespan=lifespan)


@app.post('/api/v1/products/')
async def add_product_in_db(product: ProductIn):
    articul_post = product.articul
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={articul_post}"

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url)

    if response.status_code == 200:
        data = response.json()["data"]["products"][0]
        name = data["name"]
        articul = data["id"]
        price = data["salePriceU"] / 100
        rating = data["reviewRating"]
        total = data["totalQuantity"]

        check_in_db = select(Product).filter(Product.articul == articul)
        result = await session.execute(check_in_db)
        product_in_db = result.scalars().first()

        if product_in_db:
            return {"message": "Product already exists"}

        product_to_db = Product(name=name, articul=articul, price=price, rating=rating, total=total)
        session.add(product_to_db)  # использование существующей транзакции
        await session.commit()
        return {"message": "Product added in db"}

    else:
        return {"Error": f"Error: {response.status_code}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
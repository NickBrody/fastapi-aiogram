from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram import F
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Product
from database import engine, Base, async_session

async def start_command(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Получить информацию по товару"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Введите артикул товара"
    )
    await message.answer("Введите артикул товара")


async def check_db(message: types.Message):
    articul = message.text
    async with async_session() as session:  # Создаём новую сессию для каждой операции
        check_articul = select(Product).filter(Product.articul == articul)
        result = await session.execute(check_articul)
        product_in_db = result.scalars().first()

        if product_in_db:
            response = (
                f"*Наименование товара:* {product_in_db.name}\n"
                f"*Артикул товара:* {product_in_db.articul}\n"
                f"*Цена товара:* {product_in_db.price} руб.\n"
                f"*Рейтинг товара:* {product_in_db.rating}\n"
                f"*Общее количество товара на складах:* {product_in_db.total} шт."
            )
            await message.answer(response, parse_mode="Markdown")
        else:
            await message.answer("Товар с таким артикулом не найден.")


def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command("start"))
    dp.message.register(start_command, F.text.casefold() == "получить информацию по товару")
    dp.message.register(check_db) 

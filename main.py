import asyncio
import subprocess
import logging
import sys

async def run_bot():
    """Запуск бота"""
    import bot  # Импортируем бот, чтобы он был запущен асинхронно
    await bot.main()

async def run_app():
    """Запуск FastAPI приложения"""
    import uvicorn
    from app import app  # Импортируем FastAPI приложение из app.py

    # Запуск FastAPI через Uvicorn в фоновом режиме
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Создаём задачи для бота и FastAPI
    bot_task = asyncio.create_task(run_bot())
    app_task = asyncio.create_task(run_app())

    # Ожидаем завершения обеих задач
    await asyncio.gather(bot_task, app_task)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import start
from handlers.menu import menu_handlers

# Функция конфигурирования и запуска бота
async def main():
    
    # Инициализируем бот и диспетчер
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_routers(start.router, menu_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(format='[%(asctime)s] - [%(levelname)s] - [%(message)s]', level=logging.ERROR)
    asyncio.run(main())

import asyncio
import logging
from os import getenv
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters import Command
from config import BOT_TOKEN
from handlers.start_handler import command_start_handler
from handlers.help_handler import handle_start_command
from handlers.echo_handler import echo_handler
from oauth_server import init_app
from aiohttp import web
from logger_config import setup_logging
from aiogram.types import BotCommand

setup_logging()
logger = logging.getLogger(__name__)

# Установка команд меню (опционально)
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Информация о боте"),
        BotCommand(command="/help", description="Список доступных команд"),
        BotCommand(command="/link_account", description="Привязать другой аккаунт")
    ]
    await bot.set_my_commands(commands)
    
def setup_logging():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def start_oauth_server():
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8000)
    await site.start()
    logger.info("OAuth сервер запущен на http://localhost:8000")
    while True:
        await asyncio.sleep(3600)

async def start_bot() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await set_commands(bot)

    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(handle_start_command, Command('help'))
    dp.message.register(echo_handler)

    # And the run events dispatching
    await dp.start_polling(bot)

async def main():
    logger.info("Запуск приложения...")
    setup_logging()
    bot_task = asyncio.create_task(start_bot())
    server_task = asyncio.create_task(start_oauth_server())
    await asyncio.gather(bot_task, server_task)

if __name__ == "__main__":
    asyncio.run(main())
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
from handlers.devices_handler import devices_handler
# from handlers.echo_handler import echo_handler
# from handlers.link_account_handler import command_link_account_handler
# from handlers.unlink_account_handler import unlink_account_handler
from oauth_server import init_oauth_app
from aiohttp import web
from logger_config import setup_logging
from aiogram.types import BotCommand
from database import create_db

user_sessions = {}
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

setup_logging()
logger = logging.getLogger(__name__)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Информация о боте"),
        BotCommand(command="/help", description="Список доступных команд"),
        BotCommand(command="/devices", description="Список ваших устройств"),
        # BotCommand(command="/link_account", description="Привязать аккаунт"),
        # BotCommand(command="/unlink_account", description="Отвязать аккаунт")
    ]
    await bot.set_my_commands(commands)
    
def setup_logging():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def start_oauth_server():
    app = await init_oauth_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8000)
    await site.start()
    logger.info("OAuth сервер запущен на http://localhost:8000")
    while True:
        await asyncio.sleep(3600)

async def start_bot() -> None:
    await set_commands(bot)

    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(devices_handler, Command('devices'))
    dp.message.register(handle_start_command, Command('help'))
    # dp.message.register(command_link_account_handler, Command('link_account'))
    # dp.message.register(unlink_account_handler, Command('unlink_account'))
    # dp.message.register(echo_handler)

    await dp.start_polling(bot)

async def main():
    create_db()
    logger.info("Запуск приложения...")
    setup_logging()
    bot_task = asyncio.create_task(start_bot())
    server_task = asyncio.create_task(start_oauth_server())
    await asyncio.gather(bot_task, server_task)
    
if __name__ == "__main__":
    asyncio.run(main())
from asyncio.log import logger
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import YA_URL
from config import HELLO_MESSAGE

bot = None

async def command_start_handler(message: Message) -> None:
    global bot
    bot = message.bot
    user_id = message.from_user.id
    # user_sessions[user_id] = {"state": "awaiting_auth"}

    telegram_user_id = message.from_user.id
    state = f"{telegram_user_id}"
    ya_url_with_user_id = f"{YA_URL}&state={state}"
    
    hello_mess = HELLO_MESSAGE
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Привязать яндекс умный дом', url=ya_url_with_user_id)]])
    await message.answer(
        text=hello_mess,
        reply_markup=keyboard
    )

async def notify_user_success(user_id: int):
    try:
        await bot.send_message(user_id, "Авторизация успешна! Теперь вы можете использовать бота для управления умным домом.")
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")
    
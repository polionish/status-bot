import logging
from aiogram.types import Message

async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError as e:
        logging.error(f"Ошибка в echo_handler: {e}")
        await message.answer("Nice try!")
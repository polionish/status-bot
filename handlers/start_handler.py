from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import YA_URL
from config import HELLO_MESSAGE

async def command_start_handler(message: Message) -> None:
    hello_mess = HELLO_MESSAGE
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Привязать яндекс умный дом', url=YA_URL)]])
    await message.answer(
        text=hello_mess,
        reply_markup=keyboard
    )
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import YA_URL
from config import HELLO_MESSAGE

async def command_start_handler(message: Message) -> None:
    telegram_user_id = message.from_user.id
    state = f"{telegram_user_id}"
    ya_url_with_user_id = f"{YA_URL}&state={state}"
    
    hello_mess = HELLO_MESSAGE
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Привязать яндекс умный дом', url=ya_url_with_user_id)]])
    await message.answer(
        text=hello_mess,
        reply_markup=keyboard
    )
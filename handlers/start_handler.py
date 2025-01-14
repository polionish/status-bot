from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
YA_URL = 'https://oauth.yandex.ru/authorize?response_type=code&client_id=0ef7bbdc03344ff5bebb70187541dbd9'
HELLO_MESSAGE = "Привет! Этот бот помогает узнать, что сейчас происходит с твоим умным домом. Чтобы начать пользоваться ботом, нужно привязать его к своему умному дому"

async def command_start_handler(message: Message) -> None:
    hello_mess = HELLO_MESSAGE
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Привязать яндекс умный дом', url=YA_URL)]])
    await message.answer(
        text=hello_mess,
        reply_markup=keyboard
    )
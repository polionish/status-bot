from aiogram import types

async def handle_start_command(message: types.Message):
    await message.answer("Мы вызвали для вас машину скорой помощи, ожидайте!")
from asyncio.log import logger
import requests
from aiogram import types
from aiogram.client.default import DefaultBotProperties
from database import get_tokens

bot = None

def get_devices(oauth_token):
    logger.info(f"Ваш токен: {oauth_token} щас забахаем запрос")
    url = "https://api.iot.yandex.net/v1.0/user/info"
    headers = {
        "Authorization": f"Bearer {oauth_token}"
    }
    
    response = requests.get(url, headers=headers)
    logger.info(f"!response!!!{response}")
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Ошибка: {response.status_code} {response.text}")
        return None  # Обработка ошибок

async def devices_handler(message: types.Message):
    global bot
    bot = message.bot
    user_id = message.from_user.id  
    oauth_token = get_tokens(user_id)[0]
    if oauth_token:
        data = get_devices(oauth_token)
        devices = data["devices"]
        device_names = [device["name"] for device in data["devices"]]
        logger.info(f"!!!!{devices}")
        logger.info(f"!!!!{device_names}")
        if devices:
            # devices_info = "\n".join([device['name'] for device in devices])  # Выводим названия устройств
            await message.answer(f"Ваши устройства:\n{device_names}")
        else:
            await message.answer("Не удалось получить устройства. Попробуйте позже.")
    else:
        await message.answer("Ваш аккаунт не привязан. Пожалуйста, выполните авторизацию.")

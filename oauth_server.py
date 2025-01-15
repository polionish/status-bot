import logging
from urllib.parse import parse_qs
from aiohttp import web
import aiohttp
from logger_config import setup_logging
from config import CLIENT_ID, SECRET_CLIENT, REDIRECT_URI, TOKEN_URI
from database import create_db, store_tokens, get_tokens, update_tokens
from handlers.start_handler import notify_user_success

setup_logging()
logger = logging.getLogger(__name__)

async def get_access_token(code, user_id):
    token_url = TOKEN_URI
    client_id = CLIENT_ID
    client_secret = SECRET_CLIENT
    redirect_uri = REDIRECT_URI

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(token_url, data=data) as response:
            if response.status == 200:
                token_data = await response.json()
                access_token = token_data.get('access_token')
                refresh_token = token_data.get('refresh_token')
                expires_in = token_data.get('expires_in')
                if access_token:
                    logger.info(f"Получен токен доступа: {access_token}")
                    store_tokens(user_id, access_token, refresh_token, expires_in)
                    logger.info(f"СЮДАААААААААААА get_tokens(user_id): {get_tokens(user_id)}") 
                    return access_token
                else:
                    logger.error("Не удалось получить access_token.")
            else:
                logger.error(f"Ошибка получения токена: {response.status}")
                return None

async def handle_oauth_response(request):
    logger.info("Обрабатываем OAuth-ответ...")
    params = parse_qs(request.query_string)
    code = params.get('code', [None])[0]
    tg_user_id = params.get('state', [None])[0]
    logger.info(f"Получен Telegram User ID: {tg_user_id}")
    
    if code and tg_user_id:
        logger.info(f"Получен код авторизации: {code} и идентификатор пользователя: {tg_user_id}")
        access_token = await get_access_token(code, tg_user_id)
        if access_token:
            # Сообщаем пользователю об успешной авторизации
            await notify_user_success(int(tg_user_id))
            return web.Response(text=f"Вы успешно авторизовались! Токен доступа: {access_token}")
        else:
            return web.Response(text="Не удалось получить токен. Попробуйте снова.")
    else:
        logger.warning("Код авторизации отсутствует.")
        return web.Response(text="Не получилось привязать аккаунт, повторите попытку!")

async def init_oauth_app():
    app = web.Application()
    app.router.add_get('/callback', handle_oauth_response)
    logger.info("Маршрут для OAuth сервера настроен")
    return app

def main():
    setup_logging()
    app = init_oauth_app()
    web.run_app(app, port=8000)

if __name__ == "__main__":
    main()
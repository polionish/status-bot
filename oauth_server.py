import logging
from urllib.parse import parse_qs
from aiohttp import web
from logger_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

async def handle_oauth_response(request):
    logger.info(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    params = parse_qs(request.query_string)
    code = params.get('code', [None])[0]
    if code:
        logger.info(f"Получен код авторизации: {code}")
    else:
        logger.warning("Код авторизации отсутствует.")
    return web.Response(text=f"{("Вы успешно авторизовались! Код авторизации: " + code) if code else 'Не получилось привязать аккаунт, повторите попытку!'}")

async def init_app():
    app = web.Application()
    app.router.add_get('/callback', handle_oauth_response)
    logger.info("Маршрут для OAuth сервера настроен")
    return app

def main():
    setup_logging()
    app = init_app()
    web.run_app(app, port=8000)

if __name__ == "__main__":
    main()
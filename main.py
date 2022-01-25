import argparse

from app import setup
from aiohttp import web


app = web.Application()


def parse_arguments():  # Для парсинга аргументов из командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', dest="config", help="Use config for network monitoring")
    parser.add_argument('--ssh', action="store_true", help="Monitoring network via SSH")

    return parser.parse_args()


if __name__ == "__main__":
    setup(app, parse_arguments())  # Инициализируем страницы и их функции-обработчики (хэндлеры)
    web.run_app(app)  # Запускаем собственно сайт

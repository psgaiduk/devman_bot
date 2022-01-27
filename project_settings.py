import logging
import os
from telegram import Bot
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


TOKEN_TELEGRAM = os.environ['TOKEN_TELEGRAM']
TOKEN_DEVMAN = os.environ['TOKEN_DEVMAN']
CHAT_ID = os.getenv('CHAT_ID')
BOT = Bot(token=TOKEN_TELEGRAM)
HEADERS = {'Authorization': TOKEN_DEVMAN}
URL = 'https://dvmn.org/api/long_polling/'


class BotHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        message = self.format(record)
        BOT.send_message(
            text=f'{message}',
            chat_id=CHAT_ID)


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'bot': {
            '()': BotHandler,
            'level': 'DEBUG',
            'formatter': 'std_format'
        }
    },
    'loggers': {
        'app_logger': {
            'level': 'DEBUG',
            'handlers': ['bot']
        }
    },
}

import os
from telegram import Bot
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


TOKEN_TELEGRAM = os.environ['TOKEN_TELEGRAM']
TOKEN_DEVMAN = os.environ['TOKEN_DEVMAN']
CHAT_ID = os.getenv('CHAT_ID')

HEADERS = {'Authorization': TOKEN_DEVMAN}
URL = 'https://dvmn.org/api/long_polling/'

BOT = Bot(token=TOKEN_TELEGRAM)

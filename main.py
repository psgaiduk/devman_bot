import os
from requests import get, exceptions
import time
from telegram import Bot
import logging

TOKEN_TELEGRAM = os.environ['TOKEN_TELEGRAM']
TOKEN_DEVMAN = os.environ['TOKEN_DEVMAN']
CHAT_ID = os.getenv('CHAT_ID')
bot = Bot(token=TOKEN_TELEGRAM)
headers = {'Authorization': TOKEN_DEVMAN}
url = 'https://dvmn.org/api/long_polling/'


def get_reviews(url_, headers_, params_):
    response = get(url_, headers=headers_, params=params_)
    response.raise_for_status()
    return response.json()


logging.info('Чат бот начал работу')

params = {}
while True:
    try:
        reviews = get_reviews(url, headers, params)
        if reviews.get('new_attempts'):
            timestamp = reviews['last_attempt_timestamp']
            new_attempts = reviews['new_attempts']
            for new_attempt in new_attempts:
                title = new_attempt['lesson_title']
                result = new_attempt['is_negative']
                link = new_attempt['lesson_url']
                result_text = 'Преподавтель принял вашу работу'
                if result:
                    result_text = 'Ты не справился, нужно переделать'
                bot.send_message(
                    text=f'Преподаватель проверил работу '
                    '"{title}"\n\n{result_text}\n{link}',
                    chat_id=CHAT_ID)
        else:
            timestamp = reviews['timestamp_to_request']
            params = {'timestamp': timestamp}
    except exceptions.ReadTimeout:
        pass
    except exceptions.ConnectionError:
        time.sleep(1)

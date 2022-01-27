
from requests import get, exceptions
import time
import logging.config
from project_settings import logger_config, BOT, CHAT_ID, HEADERS, URL


logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')


def get_reviews(url_, headers_, params_):
    response = get(url_, headers=headers_, params=params_)
    response.raise_for_status()
    return response.json()


logger.info('Чат бот начал работу')

params = {}
while True:
    try:
        reviews = get_reviews(URL, HEADERS, params)
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
                BOT.send_message(
                    text=f'Преподаватель проверил работу '
                    f'"{title}"\n\n{result_text}\n{link}',
                    chat_id=CHAT_ID)
        else:
            timestamp = reviews['timestamp_to_request']
            params = {'timestamp': timestamp}
    except exceptions.ReadTimeout:
        pass
    except exceptions.ConnectionError:
        time.sleep(1)

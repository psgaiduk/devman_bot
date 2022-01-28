from textwrap import dedent
from requests import get, exceptions
import time
import logging.config
from project_constants import BOT, CHAT_ID, HEADERS, URL
from logger_settings import logger_config


logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')


def get_reviews(url_, headers_, params_):
    response = get(url_, headers=headers_, params=params_)
    response.raise_for_status()
    return response.json()


def main():
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

                    text_message = f'''Преподаватель проверил работу
                    "{title}"
                    
                    {result_text}
                    {link}'''
                    BOT.send_message(
                        text=dedent(text_message),
                        chat_id=CHAT_ID)
            else:
                timestamp = reviews['timestamp_to_request']
                params = {'timestamp': timestamp}
        except exceptions.ReadTimeout as err:
            logger.error(err, exc_info=True)
        except exceptions.ConnectionError as err:
            logger.error(err, exc_info=True)
            time.sleep(1)
        except Exception as err:
            logger.error(err, exc_info=True)


if __name__ == '__main__':
    main()

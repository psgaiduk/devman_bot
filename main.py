from requests import get, exceptions
import time
import os
from telegram import Bot
from dotenv import load_dotenv
import logging

logger = logging.getLogger('app_logger')


def get_reviews(url_, headers_, params_):
    response = get(url_, headers=headers_, params=params_)
    response.raise_for_status()
    return response.json()


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    token_telegram = os.environ['TOKEN_TELEGRAM']
    token_devman = os.environ['TOKEN_DEVMAN']
    chat_id = os.getenv('CHAT_ID')

    headers = {'Authorization': token_devman}
    url = 'https://dvmn.org/api/long_polling/'

    bot = Bot(token=token_telegram)

    class BotHandler(logging.Handler):
        def __init__(self):
            logging.Handler.__init__(self)

        def emit(self, record):
            message = self.format(record)
            bot.send_message(
                text=f'{message}',
                chat_id=chat_id)

    logger.addHandler(BotHandler())
    logger.setLevel('INFO')
    logging.basicConfig(format='{asctime} - {levelname} - {name} - {message}', style='{')

    logger.info('Чат бот начал работу')

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

                    text_message = f'Преподаватель проверил работу\n' \
                                   f'"{title}"\n\n' \
                                   f'{result_text}\n' \
                                   f'{link}'
                    bot.send_message(
                        text=text_message,
                        chat_id=chat_id)
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

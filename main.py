from recognizer import Recognizer
from callbacks import CSVCallback
from config import (
    LOG_IMAGES_PATH,
    CSV_LOG_FILE_PATH,
    CHECK_IN_INTERVAL,
    REDIS_URI,
    WORKER_QUEUE,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)
from telegram import send_images_to_telegram_callback
from rq import Queue
from redis import Redis


def main():
    redis = Redis.from_url(REDIS_URI)
    queue = Queue(connection=redis, name=WORKER_QUEUE)
    send_image_callback = send_images_to_telegram_callback(
        queue=queue, chat_id=TELEGRAM_CHAT_ID, bot_token=TELEGRAM_BOT_TOKEN
    )

    csv_callback = CSVCallback(
        CSV_LOG_FILE_PATH, LOG_IMAGES_PATH, check_in_interval=CHECK_IN_INTERVAL
    )
    csv_callback.set_after_run_callback(send_image_callback)

    recognizer = Recognizer()
    recognizer.add_callback(csv_callback)

    recognizer.load_data("data.pickle")
    recognizer.run()


if __name__ == "__main__":
    main()

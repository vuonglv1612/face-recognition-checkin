from typing import Optional
import os

import requests

from logger import logger


def send_image_to_telegram(
    image_file: str, token: str, chat_id: str, caption: Optional[str] = None
):
    # check image file exists
    if not os.path.exists(image_file):
        logger.error("Image file {} does not exists".format(image_file))
        return
    try:
        url = "https://api.telegram.org/bot{}/sendPhoto".format(token)
        files = {"photo": open(image_file, "rb")}
        data = {"chat_id": chat_id}
        if caption is not None:
            data["caption"] = caption
        r = requests.post(url, files=files, data=data)
        logger.info("send image to telegram: {}".format(r.text))
    except Exception as e:
        logger.error("send image to telegram error: {}".format(e))


def send_images_to_telegram_callback(queue, bot_token, chat_id):
    def send_files(files):
        for check_in_time, username, image_file in files:
            caption = "User @{} check in at {}".format(username, check_in_time)
            queue.enqueue(
                send_image_to_telegram, image_file, bot_token, chat_id, caption
            )
            logger.info("Sending image for user {} enqueued".format(username))

    return send_files

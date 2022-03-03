import csv
import os
from datetime import datetime

import cv2
from utils import dt_to_local

from callbacks.base import Callback
from logger import logger


class CSVCallback(Callback):
    def __init__(
        self, log_file: str, image_folder: str, check_in_interval: int = 60
    ) -> None:
        self._last_check_in_time = {}
        self._check_in_interval = check_in_interval
        self._log_file = log_file
        self._image_folder = image_folder
        # create image folder if not exits
        if not os.path.exists(self._image_folder):
            os.makedirs(self._image_folder)
        self._after_run_callback = None

    def set_after_run_callback(self, callback):
        self._after_run_callback = callback

    def save_image(self, username: str, log_time: datetime, frame):
        # create subfolder if not exits
        subfolder = os.path.join(self._image_folder, username)
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        # save image
        image_file = os.path.join(subfolder, log_time.isoformat() + ".jpg")
        cv2.imwrite(image_file, frame)
        return image_file

    def run(
        self, callback_time: datetime, face_locations, face_names, frame, scale_ratio
    ):
        now = callback_time
        rows = []
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if name == "unknown":
                continue

            check_in = True
            last_check_in_time = self._last_check_in_time.get(name, None)
            if last_check_in_time is not None:
                if now.timestamp() - last_check_in_time < self._check_in_interval:
                    check_in = False

            if not check_in:
                logger.info("SKIP CHECK IN: {} BECAUSE OF INTERVAL LIMIT".format(name))
                continue
            else:
                self._last_check_in_time[name] = now.timestamp()

            top *= scale_ratio
            right *= scale_ratio
            bottom *= scale_ratio
            left *= scale_ratio

            # draw box
            clone_frame = frame.copy()
            cv2.rectangle(clone_frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # draw label
            cv2.rectangle(
                clone_frame,
                (left, bottom - 35),
                (right, bottom),
                (0, 0, 255),
                cv2.FILLED,
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                clone_frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
            )
            # save image
            image_file = self.save_image(name, now, clone_frame)
            data = (dt_to_local(now).isoformat(), name, image_file)
            logger.info("LOG DATA: {}".format(data))
            rows.append(data)
        # write to csv
        with open(self._log_file, "a") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        if self._after_run_callback is not None:
            self._after_run_callback(rows)

        return rows

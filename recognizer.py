from typing import List
import face_recognition
import cv2
import numpy as np
import pickle
from callbacks import Callback
from datetime import datetime

from utils import naive_to_aware


class Recognizer:
    def __init__(
        self, known_face_encodings=None, known_face_names=None, scale_ratio: int = 2
    ) -> None:
        self.known_face_encodings = known_face_encodings or []
        self.known_face_names = known_face_names or []
        self._callbacks: List[Callback] = []
        self._scale_ratio = scale_ratio

    def add_callback(self, callback: Callback):
        self._callbacks.append(callback)

    def load_data(self, data_file: str):
        with open(data_file, "rb") as f:
            data = pickle.load(f)
            known_face_encodings = data["encodings"]
            known_face_names = data["names"]
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names

    def run(self):
        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)

        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()
            frame_time = naive_to_aware(datetime.utcnow())

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(
                frame, (0, 0), fx=(1 / self._scale_ratio), fy=(1 / self._scale_ratio)
            )

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, face_encoding
                    )
                    name = "unknown"

                    face_distances = face_recognition.face_distance(
                        self.known_face_encodings, face_encoding
                    )
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame

            if len(face_names) > 0:
                for callback in self._callbacks:
                    callback.run(
                        frame_time,
                        face_locations,
                        face_names,
                        frame,
                        scale_ratio=self._scale_ratio,
                    )

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= self._scale_ratio
                right *= self._scale_ratio
                bottom *= self._scale_ratio
                left *= self._scale_ratio

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(
                    frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
                )
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(
                    frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
                )

            # Display the resulting image
            cv2.imshow("Video", frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

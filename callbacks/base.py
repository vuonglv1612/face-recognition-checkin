from abc import ABC, abstractmethod


class Callback(ABC):
    @abstractmethod
    def run(self, callback_time, face_locations, face_names, frame, scale_ratio):
        pass

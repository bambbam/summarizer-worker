from typing import Any
import cv2
from summarizer.domain.base import BaseImage

class Image(BaseImage):
    frame: Any
    frame_id : int

    def __init__(self, frame, frame_id):
        self.frame = frame
        self.frame_id = frame_id

    @staticmethod
    def convert_file_obj(img):
        return cv2.imencode('.jpg', img)[1].tostring()
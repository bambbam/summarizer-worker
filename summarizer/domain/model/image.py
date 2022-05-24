from typing import Any
import cv2

import numpy as np

from summarizer.domain.base import BaseDetector, BaseFeature, BaseImage
from summarizer.domain.model.detector import TinyYoloV3, YoloV3
from summarizer.domain.model.face import Face, Face_Clustering

algorithm_map = {"yolov3": YoloV3, "tinyYolov3": TinyYoloV3}


class Image(BaseImage):
    frame: Any
    frame_id : int
    #faces_in_frame : List[Face]
    #detector: BaseDetector
    face_clustering : Face_Clustering

    def __init__(self, frame, frame_id):
        self.frame = frame
        self.frame_id = frame_id
        #faces_in_frame = []
        #self.detector = algorithm_map[algorithm]()

    def extract(self, idx=0):
        #return self.detector.extract(self, idx)
        return self.face_clustering.encoding(self, idx)

    def _extract_image(self, idx=0):
        return self.detector._extract_image(self, idx)

    @staticmethod
    def convert_file_obj(img):
        return cv2.imencode('.jpg', img)[1].tostring()
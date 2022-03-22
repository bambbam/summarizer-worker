import os

import numpy as np
from imageai.Detection import ObjectDetection
from pydantic import BaseModel

from summarizer.domain.base import BaseDetector
from summarizer.domain.model.feature import Feature


class Detector(BaseDetector):
    detector = ObjectDetection()

    def extract(self, image, idx):
        detections = self.detector.detectObjectsFromImage(
            input_image=image.frame,
            input_type="array",
            minimum_percentage_probability=30,
            output_type="array",
        )
        ret = []
        for feature in detections[1]:
            ret.append(Feature(**feature, current_frame=idx))
        return ret

    def _extract_image(self, image, idx):
        detections = self.detector.detectObjectsFromImage(
            input_image=image.frame,
            input_type="array",
            minimum_percentage_probability=30,
            output_type="array",
        )
        return detections[0]


class YoloV3(Detector):
    def __init__(self, **data):
        super().__init__(**data)
        execution_path = os.getcwd()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath("./summarizer/detector_model/yolo.h5")
        self.detector.loadModel()


class TinyYoloV3(Detector):
    def __init__(self, **data):
        super().__init__(**data)
        execution_path = os.getcwd()
        self.detector.setModelTypeAsTinyYOLOv3()
        self.detector.setModelPath("./summarizer/detector_model/tiny-yolo.h5")
        self.detector.loadModel()

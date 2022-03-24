import os
from time import time
from typing import List

import numpy as np
from imageai.Detection import ObjectDetection
from pydantic import BaseModel

from summarizer.domain.base import BaseDetector, BaseFeature, BaseImage
from summarizer.domain.model.feature import Feature


class Detector(BaseDetector):
    detector = ObjectDetection()

    def extract(self, image: BaseImage, idx: int) -> List[BaseFeature]:
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

    def _extract_image(self, image: BaseImage, idx: int):
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
        start = time()
        execution_path = os.getcwd()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath("./summarizer/detector_model/yolo.h5")
        self.detector.loadModel()
        end = time()
        print(end-start)


class TinyYoloV3(Detector):
    def __init__(self, **data):
        super().__init__(**data)
        execution_path = os.getcwd()
        self.detector.setModelTypeAsTinyYOLOv3()
        self.detector.setModelPath("./summarizer/detector_model/tiny-yolo.h5")
        self.detector.loadModel()

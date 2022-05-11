from typing import Any

import numpy as np

from summarizer.domain.base import BaseDetector, BaseFeature, BaseImage
from summarizer.domain.model.detector import TinyYoloV3, YoloV3

algorithm_map = {"yolov3": YoloV3, "tinyYolov3": TinyYoloV3}


class Image(BaseImage):
    frame: Any
    detector: BaseDetector

    def __init__(self, frame, algorithm):
        self.frame = frame
        self.detector = algorithm_map[algorithm]()

    def extract(self, idx=0):
        return self.detector.extract(self, idx)

    def _extract_image(self, idx=0):
        return self.detector._extract_image(self, idx)

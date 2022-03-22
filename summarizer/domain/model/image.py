import numpy as np
from typing import Any
from summarizer.domain.base import BaseImage, BaseFeature
from summarizer.domain.model.detector import YoloV3

class Image():
    frame : Any
    detector:YoloV3 = YoloV3()

    def __init__(self, frame):
        self.frame = frame

    def extract(self, idx = 0):
        return self.detector.extract(self, idx)
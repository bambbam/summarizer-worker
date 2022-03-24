from typing import Any

import numpy as np

from summarizer.domain.base import BaseDetector, BaseFeature, BaseImage
from summarizer.domain.model.detector import TinyYoloV3, YoloV3


class Image(BaseImage):
    frame: Any
    detector: BaseDetector = YoloV3()

    def __init__(self, frame):
        self.frame = frame

    def extract(self, idx=0):
        return self.detector.extract(self, idx)

    def _extract_image(self, idx=0):
        return self.detector._extract_image(self, idx)

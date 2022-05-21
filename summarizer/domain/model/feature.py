from typing import List
#import numpy as np

from summarizer.domain.base import BaseFeature

class FrameFeature(BaseFeature):
    current_frame: int
    #percentage_probability: float
    box_points: List[int]
    #feature : np.dtype
    feature : List
    name: str

class VideoFeature(BaseFeature):
    key: str
    features: List[FrameFeature]

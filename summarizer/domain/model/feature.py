from typing import List

from summarizer.domain.base import BaseFeature


class FrameFeature(BaseFeature):
    current_frame: int
    name: str
    percentage_probability: float
    box_points: List[int]


class VideoFeature(BaseFeature):
    key: str
    features: List[FrameFeature]

from typing import List

from summarizer.domain.base import BaseFeature


class FrameFeature(BaseFeature):
    name: str
    current_frame: int
    box_points: List[int]
    # percentage_probability: float


class VideoFeature(BaseFeature):
    key: str
    features: List[FrameFeature]

from summarizer.domain.base import BaseFeature
from typing import List


class Feature(BaseFeature):
    current_frame: int
    name: str
    percentage_probability: float
    box_points: List[int]
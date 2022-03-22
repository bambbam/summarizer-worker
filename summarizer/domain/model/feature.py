from typing import List

from summarizer.domain.base import BaseFeature


class Feature(BaseFeature):
    current_frame: int
    name: str
    percentage_probability: float
    box_points: List[int]

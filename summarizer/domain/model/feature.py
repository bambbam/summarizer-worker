from typing import Dict, List

from summarizer.domain.base import BaseFeature


class FrameFeature(BaseFeature):
    name: str
    current_frame: int
    box_points: List[int]
    # percentage_probability: float


class VideoFeature(BaseFeature):
    key: str
    features: List[FrameFeature]
    representing_features: Dict[str,FrameFeature] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_best_feature(self):
        ret = {}
        for feature in self.features:
            if feature.name not in ret:
                ret[feature.name] = feature
        return ret

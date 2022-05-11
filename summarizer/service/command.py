from typing import Literal

from summarizer.infrastructure.repository import (FeatureRepository,
                                                  VideoRepository)
from summarizer.service.base import Command


class ExtractFeature(Command):
    type: Literal["ExtractFeature"]
    key: str


def extract_feature(
    command: ExtractFeature,
    feature_repo: FeatureRepository,
    video_repo: VideoRepository,
):
    video = video_repo.get(command.key)
    video_feature = video.extract_feature()
    feature_repo.put(video_feature)


COMMAND_HANDLER = {"ExtractFeature": (ExtractFeature, extract_feature)}

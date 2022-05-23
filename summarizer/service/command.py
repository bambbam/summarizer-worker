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
    try:
        video = video_repo.get(command.key)
        if video is None:
            return
        video_repo.update_status(command.key, 'start')
        ## TODO add logging
        video_feature = video.extract_feature()
        result = feature_repo.put(video_feature)
        video_repo.update_status(command.key, 'end')
        if not result :
            ...
    except:
        video_repo.update_status(command.key, 'error')
    ### TODO ADD logging


COMMAND_HANDLER = {"ExtractFeature": (ExtractFeature, extract_feature)}

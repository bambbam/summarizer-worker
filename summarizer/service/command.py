from typing import Literal

import boto3

from summarizer.domain.model.video import Video
from summarizer.infrastructure.repository import (FeatureRepository,
                                                  VideoDataRepository)
from summarizer.service.base import Command


class ExtractFeature(Command):
    type: Literal["ExtractFeature"]
    key: str

import boto3


def get_s3_url(s3, key):
    url = s3.generate_presigned_url('get_object',
                                                Params={'Bucket': 'summarizer-video',
                                                        'Key':  key},
                                                ExpiresIn=6000)
    return url

def extract_feature(
    command: ExtractFeature,
    feature_repo: FeatureRepository,
    video_repo: VideoDataRepository,
    s3,
):
    
        video_data = video_repo.get(command.key)
        if video_data is None:
            return
        video = Video(
            key=video_data.key,
            url=get_s3_url(s3, video_data.key),
            algorithm="yolov3"
        )
        
        video_repo.update_status(command.key, 'start')
        ## TODO add logging
        video_feature = video.extract_feature()
        result = feature_repo.put(video_feature)
        video_repo.put(video_data)
        if not result :
            ...
    
    
    ### TODO ADD logging


COMMAND_HANDLER = {"ExtractFeature": (ExtractFeature, extract_feature)}

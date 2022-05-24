from typing import Literal

import boto3
import numpy as np
from summarizer.domain.model.image import Image

from summarizer.domain.model.video import Video
from summarizer.infrastructure.repository import (FeatureRepository,
                                                  VideoDataRepository)
from summarizer.infrastructure.repository.s3_repository import S3Repository
from summarizer.service.base import Command
import cv2

class ExtractFeature(Command):
    type: Literal["ExtractFeature"]
    key: str

import boto3

def extract_feature(
    command: ExtractFeature,
    feature_repo: FeatureRepository,
    video_repo: VideoDataRepository,
    s3_repo: S3Repository,
):
    
        video_data = video_repo.get(command.key)
        if video_data is None:
            return
        video = Video(
            key=video_data.key,
            url=s3_repo.get_s3_url('video', video_data.key),
            algorithm="yolov3"
        )
        # feature 뽑기
        video_repo.update_status(command.key, 'start')
        video_feature = video.extract_feature()
        
        # feature 저장
        #쓰레기 코드
        video_feature.representing_features = video_feature.get_best_feature()
        extracted_feature_imgs = video.extract_box_point(video_feature.get_best_feature())
        for name, extracted_feature_img in extracted_feature_imgs.items():
            s3_repo.upload(
                Image.convert_file_obj(extracted_feature_img),
                f"img/{video_data.key}",
                name
            )
        result = feature_repo.put(video_feature)

        # 상태 업데이트
        video_repo.put(video_data)
        



COMMAND_HANDLER = {"ExtractFeature": (ExtractFeature, extract_feature)}

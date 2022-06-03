import os
from typing import List, Literal

import boto3
import numpy as np
from summarizer.domain.model.face import FaceClustering
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
        )
        # feature 뽑기
        video_repo.update_status(command.key, 'start')
        video_feature = FaceClustering().extract_feature(video)

        extracted_feature_imgs = video.extract_box_point(video_feature.get_best_feature())
        for name, extracted_feature_img in extracted_feature_imgs.items():
            s3_repo.upload(
                Image.convert_file_obj(extracted_feature_img),
                f"img/{video_data.key}",
                name
            )
        ## TODO 잘못짬~~
        result = feature_repo.put(video_feature)
        if not result:
            print("error!")
        # 상태 업데이트
        video_repo.put(video_data)
        

class ShortenVideo(Command):
    type: Literal["ShortenVideo"]
    key: str
    must_include_feature: List[str]
    
def shorten_video(
    command: ShortenVideo,
    feature_repo: FeatureRepository,
    video_repo: VideoDataRepository,
    s3_repo: S3Repository,
):
    feature = feature_repo.get(command.key)
    if feature is None:
        return
    video_data = video_repo.get(command.key)
    video = Video(
            key=command.key,
            url=s3_repo.get_s3_url('video', command.key),
        )
    tmp_s3_video_label, s3_video_label = video.shorten(
        video_feature=feature,
        must_include_feature=command.must_include_feature
    )
    s3_repo.upload_video(
                s3_video_label,
                f"shorten_video",
                command.key,
            )    
    
    video_repo.put(video_data, "end")
    os.remove(tmp_s3_video_label)
    os.remove(s3_video_label)

COMMAND_HANDLER = {
    "ExtractFeature": (ExtractFeature, extract_feature), 
    "ShortenVideo":(ShortenVideo, shorten_video)
}

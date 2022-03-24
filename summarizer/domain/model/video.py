from operator import concat
from typing import Any, Dict, Generator, List

import cv2

from summarizer.domain.base import BaseFeature, BaseImage, BaseVideo
from summarizer.domain.model.feature import Feature
from summarizer.domain.model.image import Image
import sys


class Video(BaseVideo):
    url: str
    parameter: Dict = {}
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cap = cv2.VideoCapture(self.url)
        self.parameter = {
            "length" : int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "width" : int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height" : int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps" : cap.get(cv2.CAP_PROP_FPS),
        }
        cap.release()

    def extract_feature(self) -> List[BaseFeature]:
        ret = []
        parameter = self._get_parameter()
        images = self._read_video()
        for idx, image in images:
            if(idx%parameter["fps"]==0):
                ret.extend(image.extract(idx))
        return ret

    def shorten(self, video_feature: List[Feature], must_include_feature: List[str]):
        parameter = self._get_parameter()
        images = self._read_video()
        fps = parameter["fps"]
        one_sec_images = []
        to_concat_timeframe = []
        concated_image = []
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter("out.avi", fourcc, fps, (parameter["width"], parameter["height"]))
        
        for feature in video_feature:
            ch = False  
            for x in must_include_feature:
                if x == feature.name:
                    ch = True
                    break
            if ch:
                to_concat_timeframe.append(feature.current_frame)
        
        for idx, image in images:
            one_sec_images.append(image)
            if(idx%fps == 0):
                if(idx in to_concat_timeframe):
                    concated_image.extend(one_sec_images)
                one_sec_images = []

        for image in concated_image:
            out.write(image.frame)
        out.release()
        
        
        

    def _read_video(self):
        idx = 0
        cap = cv2.VideoCapture(self.url)
        parameter = self._get_parameter()
        self._print_parameter()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            yield (int(cap.get(1)), Image(frame=frame))
        cap.release()

    def _get_parameter(self):
        return self.parameter

    def _print_parameter(self):
        print("length :", self.parameter["length"])
        print("width :", self.parameter["width"])
        print("height :", self.parameter["height"])
        print("fps :", self.parameter["fps"])

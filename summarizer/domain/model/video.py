from operator import concat
from typing import Any, Generator, List

import cv2

from summarizer.domain.base import BaseFeature, BaseImage, BaseVideo
from summarizer.domain.model.feature import Feature
from summarizer.domain.model.image import Image


class Video(BaseVideo):
    url: str
    cap: Any

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cap = cv2.VideoCapture(self.url)

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
        out = cv2.VideoWriter("out.mp4", fourcc, fps, (parameter["width"], parameter["height"]))
        
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
        parameter = self._get_parameter()
        self._print_parameter(parameter)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            yield (int(self.cap.get(1)), Image(frame=frame))
        self.cap.release()

    def _get_parameter(self):
        length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        return {"length": length, "width": width, "height": height, "fps": fps}

    def _print_parameter(self, parameter):
        print("length :", parameter["length"])
        print("width :", parameter["width"])
        print("height :", parameter["height"])
        print("fps :", parameter["fps"])

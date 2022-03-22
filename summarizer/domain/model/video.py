from typing import Generator, List
import cv2

from summarizer.domain.base import BaseVideo, BaseFeature, BaseImage
from summarizer.domain.model.image import Image

class Video(BaseVideo):
    url: str
    def _read_video(self):
        idx = 0
        cap = cv2.VideoCapture(self.url)
        while(cap.isOpened()):
            ret, frame = cap.read()
            yield Image(frame=frame)
        cap.release()


    def extract_feature(self) -> List[BaseFeature]:
        ret = []
        images = self._read_video()
        for idx, image in enumerate(images):
            ret.extend(image.extract(idx))
        return ret

    def shorten(feature: BaseFeature):
        ...

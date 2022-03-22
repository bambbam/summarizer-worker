from typing import Generator, List
import cv2

from summarizer.domain.base import BaseVideo, BaseFeature, BaseImage
from summarizer.domain.model.image import Image

class Video(BaseVideo):
    url: str

    def _get_parameter(self, cap):
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        return {
            "length": length,
            "width": width,
            "height": height,
            "fps": fps
        }

    def _read_video(self):
        idx = 0
        cap = cv2.VideoCapture(self.url)

        parameter = self._get_parameter(cap)
        print("length :", parameter["length"])
        print("width :", parameter["width"])
        print("height :", parameter["height"])
        print("fps :", parameter["fps"])

        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break
            if(int(cap.get(1)) % parameter["fps"] == 0):
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

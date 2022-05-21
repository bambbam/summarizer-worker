from typing import List

from imageai.Detection import ObjectDetection
from summarizer.domain.base import BaseDetector, BaseImage, singleton
from summarizer.domain.model.feature import FrameFeature


class Detector(BaseDetector):
    detector = ObjectDetection()
    

    def extract(self, image: BaseImage, idx: int) -> List[FrameFeature]:
        # iamge는 왜 type이 BaseImage?, 그리고 image의 변수들은 저절로 detector로 전해짐?
        detections = self.detector.detectObjectsFromImage(
            input_image=image.frame,
            input_type="array",
            minimum_percentage_probability=30,
            output_type="array",
        )
       # print(detections)
       # print(len(detections[1]))
       # print(len(detections[1][0]))
        #detection에 제일 중요한 object에 대한 feature 값이 없음
        ret = []
        for feature in detections[1]:
            ret.append(FrameFeature(**feature, current_frame=idx))
        return ret

    def _extract_image(self, image: BaseImage, idx: int):
        detections = self.detector.detectObjectsFromImage(
            input_image=image.frame,
            input_type="array",
            minimum_percentage_probability=30,
            output_type="array",
        ) #실제로 object detection을 하는 곳
        return detections[0]

@singleton
class YoloV3(Detector):
    def __init__(self, **data):
        super().__init__(**data)
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath("./summarizer/detector_model/yolo.h5")
        self.detector.loadModel()

@singleton
class TinyYoloV3(Detector):
    def __init__(self, **data):
        super().__init__(**data)
        self.detector.setModelTypeAsTinyYOLOv3()
        self.detector.setModelPath("./summarizer/detector_model/tiny-yolo.h5")
        self.detector.loadModel()


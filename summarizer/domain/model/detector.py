import numpy as np
import os
from summarizer.domain.base import Singleton
from pydantic import BaseModel
from imageai.Detection import ObjectDetection
from summarizer.domain.model.Feature import Feature

class YoloV3(BaseModel):
    class Config():
        arbitrary_types_allowed=True
    
    detector = ObjectDetection()
    
    def __init__(self,**data):
        super().__init__(**data)
        execution_path = os.getcwd()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath("./summarizer/detector_model/yolo.h5")
        self.detector.loadModel()
    
    def extract(self, image, idx):
        detections = self.detector.detectObjectsFromImage(input_image=image.frame, input_type="array", minimum_percentage_probability=30, output_type="array")
        ret = []
        for feature in detections[1]:
            ret.append(Feature(**feature, current_frame=idx))
        return ret

    def _extract_image(self, image, idx):
        detections = self.detector.detectObjectsFromImage(input_image=image.frame, input_type="array", minimum_percentage_probability=30, output_type="array")
        return detections[0]
from typing import  Dict, List

import cv2

from summarizer.domain.base import BaseVideo
from summarizer.domain.model.feature import FrameFeature, VideoFeature
from summarizer.domain.model.image import Image



class Video(BaseVideo):
    key: str
    url: str
    parameter: Dict = {}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) # 부모 메소드, 변수 등 상속, 대충 변수들 초기화 해줌
        cap = cv2.VideoCapture(self.url) # 동영상 열기
        self.parameter = {
            "length": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": int(cap.get(cv2.CAP_PROP_FPS)),
        }
        cap.release()

    def shorten(self, video_feature: VideoFeature, must_include_feature: List[str]):
        parameter = self._get_parameter()
        images = self._read_video()
        fps = parameter["fps"]
        one_sec_images = []
        to_concat_timeframe = []
        concated_image = []
        fourcc = cv2.VideoWriter_fourcc(*"DIVX")
        out = cv2.VideoWriter(
            "out.avi", fourcc, fps, (parameter["width"], parameter["height"])
        )
        for feature in video_feature.features:
            ch = False  
            for x in must_include_feature: #??
                if x == feature.name: # 특정 인물 
                    ch = True
                    break #흠
            if ch:
                to_concat_timeframe.append(feature.current_frame) # 프레임 번호 저장
        
        for idx, image in images:
            one_sec_images.append(image)
            if(idx%fps == 0):
                if(idx in to_concat_timeframe): # 사람이 있는 프레임 번호라면 
                    concated_image.extend(one_sec_images) # 대충 기준 시간마다 이미지를 출력하고 다시 초기화
                one_sec_images = []

        for image in concated_image:
            out.write(image.frame)
        out.release()

    def extract_box_point(self, features:Dict[str,FrameFeature]):
        ret = {}
        cap = cv2.VideoCapture(self.url)
        for name, feature in features.items():
            cap.set(1,int(feature.current_frame))
            _, frame = cap.read()
            t,r,b,l = feature.box_points
            frame = frame[t:b, l:r]
            ret[name] = frame
        return ret

    def _read_video(self):
        cap = cv2.VideoCapture(self.url)
        if not cap.isOpened():
            print("video not opened!")
        frame_id = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            #yield (int(cap.get(1)), Image(frame=frame, algorithm=self.algorithm))
            yield (frame_id, Image(frame=frame, frame_id=frame_id))
            frame_id += 1
        cap.release()

    def _get_parameter(self):
        return self.parameter

    def _print_parameter(self):
        print("length :", self.parameter["length"])
        print("width :", self.parameter["width"])
        print("height :", self.parameter["height"])
        print("fps :", self.parameter["fps"])

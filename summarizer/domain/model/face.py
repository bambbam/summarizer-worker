import cv2
import face_recognition
import numpy as np
from sklearn.cluster import DBSCAN #clustering에 필요 

from summarizer.domain.base import BaseImage
from summarizer.domain.model.feature import FrameFeature

class Face():
  def __init__(self, frame_id, box, feature, name = None):
    self.frame_id = frame_id
    self.box = box #얼굴 영역
    self.feature = feature #128차 얼굴 feature
    self.name = name

class Face_Clustering():
    def __init__(self):
        self.faces = []
        self.unique_cnt_dict = {}
        self.person_class = 0

    def encoding(self, image:BaseImage, idx:int):
        rgb_frame = image.frame[:,:,::-1] #BGR을 RGB 순으로 바꾸기
        face_box = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_box)
        # face_box.shape (top, right, bottom, left, face_개수)
        #face_encodings.shape (128 vector, face_개수)
        if not face_box:
            print("no face in this face id : %d" %idx)
            return
        # continue
        faces_in_frame = [] #feces_in_frame에 FrameFeature class 저장
        for box, encodings in zip(face_box, face_encodings):
            face = FrameFeature(idx, box, encodings, name=None)
            faces_in_frame.append(face)
        # self.drawBox(frame, face)

        self.faces.extend(faces_in_frame) #extend는 iterable한것들을 append
        return faces_in_frame

    def cluster(self):
        if len(self.faces) == 0:
            return
        features = [face.feature for face in self.faces]

        cm = DBSCAN(metric="euclidean")
        cm.fit(features)
        # clustering 완료

        label_ids, count = np.unique(cm.labels_, return_counts=True) #0부터 labeling, -1은 분류되지 않은 encoding
        self.unique_cnt_dict = dict(zip(label_ids, count)) # 레이블당 프레임수
        self.person_class = len(label_ids) - 1 #사람 종류

        for label_id in label_ids:
            index = np.where(cm.labels_ == label_id)[0]
            for i in index:
                frame_id = self.faces[i].frame_id
                box = self.faces[i].box
                feature = self.faces[i].feature
                
        print('clustering done')
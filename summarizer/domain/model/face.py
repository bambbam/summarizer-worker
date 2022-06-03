from typing import List
import cv2
import face_recognition
import numpy as np
from sklearn.cluster import DBSCAN #clustering에 필요 
from sklearn.decomposition import PCA

from summarizer.domain.base import BaseImage, BaseVideo
from summarizer.domain.model.feature import FrameFeature, VideoFeature
from summarizer.domain.model.image import Image
from summarizer.domain.model.video import Video

def dist(face1, face2):
    return np.linalg.norm(face1-face2)


class FaceClustering():
    def extract_feature(self, video:Video):
        features = []
        faces = []     
        parameter = video._get_parameter()
        num_modular = 3
        for idx, img in video._read_video():
            if idx % num_modular == 0:
                print(idx)
                face_encodings, faces_in_frame = self.encoding(img, idx)
                features.extend(face_encodings)
                faces.extend(faces_in_frame)

        faces, core_sample_indices_ = self.cluster(features, faces)
        
        representing_feature = {}
        for idx in core_sample_indices_:
            representing_feature[faces[idx].name] = faces

        ret = VideoFeature(key=video.key, features=faces)
        ret.representing_features = ret.get_best_feature()
        return ret
        


    def encoding(self, image:Image, idx:int):
        rgb_frame = image.frame[:,:,::-1] #BGR을 RGB 순으로 바꾸기
        face_box = face_recognition.face_locations(rgb_frame, model="cnn")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_box)
        print("# face : ", len(face_box))
        # face_box.shape (top, right, bottom, left, face_개수)
        #face_encodings.shape (128 vector, face_개수)
        if not face_box:
            print("no face in this face id : %d" %idx)
            return ([], [])
        # continue
        faces_in_frame = [] #feces_in_frame에 FrameFeature class 저장
        for box, encodings in zip(face_box, face_encodings):
            box_list = list([int(x) for x in box])
            face = FrameFeature(name='', current_frame=int(idx), box_points=box_list)
            faces_in_frame.append(face)
        # self.drawBox(frame, face)
        return (face_encodings, faces_in_frame)

    def cluster(self, features, faces:List[FrameFeature]):
        if len(faces) == 0:
            return

        cm = DBSCAN(eps=0.3, min_samples=15, metric=dist)
        cm.fit(features)
        # clustering 완료

        label_ids, count = np.unique(cm.labels_, return_counts=True) #0부터 labeling, -1은 분류되지 않은 encoding
        print(label_ids, count, len(faces))
        # unique_cnt_dict = dict(zip(label_ids, count)) # 레이블당 프레임수
        # person_class = len(label_ids) - 1 #사람 종류
        for label_id in label_ids:
            index = np.where(cm.labels_ == label_id)[0]
            for i in index:
                #frame_id = self.faces.features[i].frame_id
                #box = self.faces.features[i].box
                #feature = self.faces.features[i].feature
                faces[i].name = str(label_id)
        print('clustering done')
        return faces, cm.core_sample_indices_


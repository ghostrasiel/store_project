import mtcnn
import cv2
import tensorflow as tf
import os
import numpy as np
import PIL
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import normalize
import joblib
from opencv.FACE.model import mysql



class face_model_py():
    def __init__(self ,  model_path=f'{os.getcwd()}/model/facenet_keras.h5'):
        self.detector = mtcnn.MTCNN()
        self.face_model = tf.keras.models.load_model(model_path, compile=False)
        self.member_list = mysql.check_member()

    #檢查是否為臉部
    def check_face(self , img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pixels = np.asarray(img)
        results = self.detector.detect_faces(pixels)
        if len(results) != 0 :
            x1, y1, w, h = results[0]['box']
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + w, y1 + h
            face_list = [x1, y1, x2, y2]
            return face_list
        else:
            return None
    #創建模型
    def face_MTCNN(self, resize=(160, 160)):
        img_list = []
        label = []
        for member in self.member_list:
            img = cv2.imread(member[4])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pixels = np.asarray(img)
            results = self.detector.detect_faces(pixels)
            x1, y1, w, h = results[0]['box']
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + w, y1 + h
            face = pixels[y1:y2, x1:x2]
            image = PIL.Image.fromarray(face)
            image = image.resize(resize)
            face_array = np.asarray(image)
            img_list.append(face_array)
            label.append(member[0] - 1)
            for _ in range(20):
                up_img = tf.image.random_flip_up_down(face_array)
                right_img = tf.image.random_flip_left_right(up_img)
                img_list.append(right_img)
                label.append(member[0] - 1)
                print(member[2], right_img.shape)
        train = np.asarray(img_list)
        target = np.asarray(label)
        return train, target

    def face_pixes(self , x):
        train = x.astype('float32')
        mean, std = train.mean(), train.std()
        face_pixes = (train - mean) / std
        return face_pixes

    def build_model(self , build_path='./model/face_model.pkl'):
        train, target = self.face_MTCNN()
        x_train, x_test, y_train, y_test = train_test_split(train, target, train_size=0.8, random_state=1)
        x_train_pixes = self.face_pixes(x_train)
        x_test_pixes = self.face_pixes(x_test)
        x_train_yhat = self.face_model.predict(x_train_pixes)
        x_test_yhat = self.face_model.predict(x_test_pixes)
        #正則化
        x_train_norm = normalize(x_train_yhat, norm='l2')
        x_test_norm = normalize(x_test_yhat, norm='l2')
        # 將臉部特徵轉換為128個特徵向量
        # print('x_train:', x_train_yhat.shape)
        # print('x_test:', x_test_yhat.shape)
        model = SVC(kernel='linear', C=0.5 , gamma='auto')
        model.fit(x_train_norm, y_train)
        y_pred = model.predict(x_test_norm)
        print('score:', accuracy_score(y_test, y_pred))
        joblib.dump(model, build_path )

    #預測資料
    def facenet_one_photo(self , img, resize=(160, 160)):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pixels = np.asarray(img)
        results = self.detector.detect_faces(pixels)
        x1, y1, w, h = results[0]['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + w, y1 + h
        face = pixels[y1:y2, x1:x2]
        image = PIL.Image.fromarray(face)
        image = image.resize(resize)
        face_array = np.asarray(image)
        face_array = face_array.astype('float32')
        mean, std = face_array.mean(), face_array.std()
        face_pixes = (face_array - mean) / std
        face_pixes = np.expand_dims(face_pixes, axis=0)
        y_hat = self.face_model.predict(face_pixes)
        return y_hat

    def predict_photo(self , img , model_path=f'{os.getcwd()}/model/face_model.pkl' ):
        e_list = []
        p_hat = None
        model = joblib.load(model_path)
        photo_hat = self.facenet_one_photo(img=img)
        y_hat_norm = normalize(photo_hat, norm='l2')
        for m in self.member_list:
            member_array = np.frombuffer(m[3], dtype='float32')
            e = round(np.linalg.norm(photo_hat[0] - member_array), 2)
            e_list.append(e)

        for e_tag in e_list:
            if e_tag < 9:
                print('臉部接近值:' , e_tag)
                p_hat = model.predict(y_hat_norm)
                break

        if p_hat != None:
            result = mysql.select_member(int(p_hat[0]) + 1)[0]
        else:
            result = None

        return result


if __name__ == '__main__':
    face_model = face_model_py(model_path='./facenet_keras.h5')
    #預測單張
    # img = cv2.imread('./eric2.jpg')
    # result = face_model.predict_photo(img , model_path='./face_model.pkl')
    # print(result)
    #建立模型
    face_model.build_model(build_path='./face_model.pkl')

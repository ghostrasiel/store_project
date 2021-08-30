import cv2
import numpy as np
from retinaface import  RetinaFace
import tensorflow as tf
import os

class mask_model():
    def __init__(self , model_path=f'{os.getcwd()}/model/mask_model.h5'):
        self.dec = RetinaFace(quality="noraml")
        self.model = tf.keras.models.load_model(model_path)

    def Detect_mask(self , img ,mask_text = 'Do you wear a mask?' ):
        detections = self.dec.predict(img)
        if len(detections) >= 1:
            x1 = detections[0]['x1']
            y1 = detections[0]['y1']
            x2 = detections[0]['x2']
            y2 = detections[0]['y2']
            face = img[y1:y2, x1:x2]
            face = cv2.resize(face, (128, 128))
            smail_face = face.copy()
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = face / 255.0
            face = np.asarray(face)
            face = np.expand_dims(face, axis=0)
            y_pred = self.model.predict(face)
            result = np.argmax(y_pred)
            if result == 1:
                mask_text = 'NO! You not wear a mask'
            else:
                mask_text = 'Yes! very good!'
        else:
            mask_text = '...'
            smail_face = np.zeros((128, 128, 3), dtype=np.uint8)
        return smail_face , mask_text

    def grab_face(self , img):
        detections = self.dec.predict(img)
        if len(detections) >= 1:
            x1 = detections[0]['x1']
            y1 = detections[0]['y1']
            x2 = detections[0]['x2']
            y2 = detections[0]['y2']
            return [x1,y1,x2,y2]



if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3 ,600)
    cap.set(4 ,400)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    p_list = []
    mask_model = mask_model(model_path='./mask_model.h5')
    mask_text = 'Do you wear a mask?'
    while True :
        put = np.zeros((260, 640, 3), dtype=np.uint8)
        _ , img = cap.read()
        if count > 40 :
            face , mask_text = mask_model.Detect_mask(img , mask_text=mask_text)
            img[0:128, 0:128] = face


        cv2.putText(put, mask_text, (130, 104), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
        new_img = np.vstack((img , put))
        cv2.imshow('video', new_img)
        count += 1
        if cv2.waitKey(10) & 0xFF == ord('p'):
            break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
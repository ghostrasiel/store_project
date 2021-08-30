import cv2
import numpy as np
from retinaface import  RetinaFace
import tensorflow as tf
cap = cv2.VideoCapture(0)
cap.set(3 ,600)
cap.set(4 ,400)
FPS = cap.get(cv2.CAP_PROP_FPS)
count = 0
p_list = []
dec = RetinaFace(quality="noraml")
model = tf.keras.models.load_model('mask_model.h5')
mask_text = 'Do you wear a mask?'
while True :
    print(count)
    put = np.zeros((260, 640, 3), dtype=np.uint8)
    _ , img = cap.read()
    detections = dec.predict(img)
    print(detections)
    if len(detections) >= 1 :
        x1 = detections[0]['x1']
        y1 = detections[0]['y1']
        x2 = detections[0]['x2']
        y2 = detections[0]['y2']
        face = img[y1:y2, x1:x2]
        face = cv2.resize(face , (128 , 128))
        img[0:128 , 0:128] = face
        mask_text = 'Do you wear a mask?'
        if count > 40 :
            face = cv2.cvtColor(face , cv2.COLOR_BGR2RGB)
            face = face / 255.0
            face = np.asarray(face)
            face = np.expand_dims(face, axis=0)
            y_pred = model.predict(face)
            result = np.argmax(y_pred)
            if result == 1 :
                mask_text = 'NO! You not wear a mask'
            else:
                mask_text = 'Yes! very good!'
    else:
        mask_text = '...'
        count = 30

    cv2.putText(put, mask_text, (130, 104), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
    new_img = np.vstack((img , put))
    cv2.imshow('video', new_img)
    count += 1
    if cv2.waitKey(10) & 0xFF == ord('p'):
        break


cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
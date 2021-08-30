import cv2
from model import request_face , mysql
import uuid
import os
import numpy as np

dirPath=f'{os.getcwd()}\\data\\'
name = 'Kelly'
#uuid 建立會員id
member_id = uuid.uuid1()
picture_path = dirPath + name +'\\' + f'{name}.jpg'
face_model = request_face.face_model_py()
img = cv2.imread(picture_path)
face_list  = face_model.check_face(img)

if face_list != None:
    face_array1 = face_model.facenet_one_photo(img)
    #轉換成二進制
    arr = face_array1.tostring()
    values = [(member_id , name , arr ,picture_path )]
    # mysql.add_member(values)
else:
    print('無法辨識該照片')





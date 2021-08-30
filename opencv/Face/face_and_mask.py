import cv2
import numpy as np
from model import request_face , request_mask , kafka_py ,mysql , Alarm_system
import datetime
import time
import os
import sys

def main(mode , register_id=None):
    mask_model = request_mask.mask_model()
    hold_num = 0
    register_user = mysql.check_register(register_id=register_id)
    register_user_state = register_user[0][1]
    while True:
        try:
            cap = cv2.VideoCapture(0)
            cap.set(3 ,600)
            cap.set(4 ,400)
            count = 0
            p_list = []
            face_model = request_face.face_model_py()
            mask_text = 'Do you wear a mask?'
            good_mask = 0 #通關有戴口罩
            good_mask_num = 0 #製造通關口罩延遲
            not_mask = 1 #通關拔除口罩
            not_mask_num = 0 #製造拔除口罩延遲
            check_mask = 0 #通過有戴口罩
            traffic = 0 #傳送kafka資料
            face = np.zeros((128 , 128 , 3), dtype=np.uint8)

            create_model_time= os.path.getmtime('./model/face_model.pkl')
            create_model_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(create_model_time))
            print(create_model_time)
            if hold_num == 1:
                cv2.destroyAllWindows()
                hold_num = 0

            while True :
                # print(count)
                put = np.zeros((260, 640, 3), dtype=np.uint8)
                _ , img = cap.read()
                face_list = mask_model.grab_face(img)
                if mode == 'Cash_register' :
                    if face_list != None:
                        if int(count)%50 == 0 :
                            register_user = mysql.check_register(register_id=register_id)
                            register_user_state = register_user[0][1]
                else:
                    register_user_state = 'None'

                if register_user_state == 'None' :
                    cv2.putText(put, f'Please someone', (190, 44), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0 , 255), 1, cv2.LINE_AA)
                    try:
                        if face_list != None:
                            if count > 10 and good_mask == 0:
                                face, mask_text = mask_model.Detect_mask(img, mask_text=mask_text)
                                if mask_text == 'Yes! very good!':
                                    good_mask_num += 1
                                    if good_mask_num >= 5:
                                        good_mask = 1
                                        count = 50
                            cv2.putText(put, mask_text, (130, 84), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
                            if good_mask == 1 :
                                if not_mask == 1:
                                    _, not_mask_text = mask_model.Detect_mask(img, mask_text=mask_text)
                                    cv2.putText(put, 'Please take off the mask', (130, 104), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
                                    if not_mask_text == 'NO! You not wear a mask':
                                        not_mask_num += 1
                                        if not_mask_num >= 10 :
                                            not_mask = 0
                                            count = 50
                                if not_mask == 0 and count >= 55 :
                                    if count >= 80 and len(p_list) == 0 :
                                        try:
                                            face_list = face_model.check_face(img)
                                            print(face_list)
                                            if face_list != None :
                                                cv2.rectangle(img, (face_list[0], face_list[1]), (face_list[2], face_list[3]), (0, 255, 0), 3)
                                                result = face_model.predict_photo(img)
                                                print(result)
                                                if result != None:
                                                    p_list.append(result)
                                                    #會員id
                                                    cv2.putText(img, result[1][0:10] + '...', (face_list[0], face_list[1] - 10), cv2.FONT_HERSHEY_PLAIN,0.8, (0, 255, 0), 2, cv2.LINE_AA)
                                                    #會員名字
                                                    cv2.putText(img, result[2], (face_list[0], face_list[1] - 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0),2, cv2.LINE_AA)
                                                else:
                                                    p_list.append('not number')
                                                    cv2.putText(img, 'is not member', (face_list[0], face_list[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1,(0, 255, 0), 2, cv2.LINE_AA)
                                        except:
                                            pass
                                    elif count >= 80 :
                                        if face_list != None:
                                            cv2.rectangle(img, (face_list[0], face_list[1]), (face_list[2], face_list[3]), (0, 255, 0), 3)
                                            if p_list[0] != 'not number':
                                                cv2.putText(img,  result[1][0:10] + '...', (face_list[0], face_list[1] - 10), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
                                                cv2.putText(img, result[2], (face_list[0], face_list[1] - 20), cv2.FONT_HERSHEY_PLAIN, 1,(0, 255, 0), 1, cv2.LINE_AA)
                                                cv2.putText(put, f'Hi,{result[2]} Welocme!', (130,124), cv2.FONT_HERSHEY_PLAIN, 2,(0, 255, 0), 1, cv2.LINE_AA)
                                                if check_mask == 0:
                                                    _, check_mask_text = mask_model.Detect_mask(img, mask_text=mask_text)
                                                    cv2.putText(put, 'Wait! Please wear a mask ', (130, 154), cv2.FONT_HERSHEY_PLAIN, 2,(0, 255, 0), 1, cv2.LINE_AA)
                                                    if check_mask_text == 'Yes! very good!':
                                                        check_mask = 1
                                                elif check_mask == 1 :
                                                    if mode == 'Entrance' :
                                                        cv2.putText(put, 'GO,GO ,Shopping', (130, 154), cv2.FONT_HERSHEY_PLAIN, 2,(0, 255, 0), 1, cv2.LINE_AA)
                                                        if traffic == 0:
                                                            now = datetime.datetime.today()
                                                            now = now.strftime('%Y/%m/%d %H:%M:%S')
                                                            data = {'time': str(now), 'user_id': result[1], 'name': result[2]}
                                                            kafka_py.kafka_traffic('people_traffic', data)
                                                            traffic = 1
                                                    elif mode == 'Cash_register' :
                                                        cv2.putText(put, 'Please start scanning', (130, 154), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
                                                        cv2.putText(put, 'the product', (130, 174), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
                                                        if traffic == 0:
                                                            mysql.update_register(register_id=register_id , user = result[1])
                                                            traffic = 1
                                            else:
                                                cv2.putText(img, 'is not member', (face_list[0], face_list[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1,
                                                            (0, 255, 0), 1, cv2.LINE_AA)
                                                cv2.putText(put, f'Please join the member', (130, 124), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
                                                check_model_time = os.path.getmtime('./model/face_model.pkl')
                                                check_model_time = time.strftime("%Y/%m/%d %H:%M:%S",
                                                                                 time.localtime(check_model_time))
                                                if check_model_time != create_model_time:
                                                    break
                                    else:
                                        cv2.rectangle(img, (215, 50), (435, 257), (0, 0 , 255), 3)
                                        cv2.putText(img, 'Put your face here', (215, 50-10), cv2.FONT_HERSHEY_PLAIN, 1 ,(0, 0 ,255), 1, cv2.LINE_AA)
                                        cv2.putText(put, f'Put in the red box', (130 , 104), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
                        else:
                            count = 40
                            mask_text = None
                            not_mask_text = None
                            check_mask_text = None
                            good_mask = 0
                            not_mask = 1
                            check_mask = 0
                            face = np.zeros((128, 128, 3), dtype=np.uint8)
                            p_list = []
                            traffic = 0
                            not_mask_num = 0
                            good_mask_num = 0
                            check_model_time = os.path.getmtime('./model/face_model.pkl')
                            check_model_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(check_model_time))
                            if check_model_time != create_model_time:
                                break

                    except:
                        count = 0
                        mask_text = None
                        not_mask_text = None
                        check_mask_text = None
                        good_mask = 0
                        not_mask = 1
                        check_mask = 0
                        face = np.zeros((128, 128, 3), dtype=np.uint8)
                        p_list = []
                        traffic = 0
                        not_mask_num = 0
                        good_mask_num = 0
                        check_model_time = os.path.getmtime('./model/face_model.pkl')
                        check_model_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(check_model_time))
                        if check_model_time != create_model_time :
                            break
                else:
                    cv2.putText(put, f'Please wait for the previous customer', (65, 64), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.putText(put, f'to complete the checkout', (65, 104),cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 1, cv2.LINE_AA)
                    mask_text = None
                    not_mask_text = None
                    check_mask_text = None
                    good_mask = 0
                    not_mask = 1
                    check_mask = 0
                    face = np.zeros((128, 128, 3), dtype=np.uint8)
                    p_list = []
                    traffic = 0
                    not_mask_num = 0
                    good_mask_num = 0
                    check_model_time = os.path.getmtime('./model/face_model.pkl')
                    check_model_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(check_model_time))
                    if check_model_time != create_model_time:
                        break

                img[0:128, 0:128] = face
                new_img = np.vstack((img , put))
                cv2.imshow('video', new_img)
                count += 1
                if cv2.waitKey(10) & 0xFF == ord('p'):
                    break

            cap.release()
            cv2.destroyAllWindows()
            cv2.waitKey(1)

            hold_img = np.zeros((260, 1080, 3), dtype=np.uint8)
            cv2.putText(hold_img, f'Please wait while the information is updated', (130, 124), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.imshow('wait', hold_img)
            hold_num = 1
            cv2.waitKey(1)

        except:
            Alarm_system.err_line_push('人臉辨識',msg =f'{sys.exc_info()[0]}\n{sys.exc_info()[1]}')


if __name__ == '__main__':
    #更換模式
    mode = 'Entrance'  #入口模式
    # mode = 'Cash_register' #收銀模式
    main(mode=mode , register_id='A')





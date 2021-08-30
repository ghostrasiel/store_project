# 疫Shopping 無人商店系統專案
## 專案簡介:
此專案結合在疫情期間為減少人與人之間的接觸,於是在此之下規劃出一個全自動化的商店系統,供顧客在購買時完全自助式使用
在此之下我們專住在設計人臉/口罩辨識、人流辨識、物品辨識、線上資料流及時串接及分析產品銷售狀況、以及顧客如何進店及提供個人資訊
並在這之下透過Kaggle消費資訊來實現資料分析  
在這專案我主要負責項目為：
* 資料庫的建置、連結及資料庫導入API撰寫
* 資料產品爬蟲
* 資料清洗
* 口罩 / 人臉辨識系統
* Kafka建置及API導入
* Linebot建置
* 警報設置
## 專案架構圖:
![image](https://user-images.githubusercontent.com/58453878/131308079-b1362717-b9fa-4b07-8079-4708ff74774d.png)
## 商店架構圖:
![image](https://user-images.githubusercontent.com/58453878/131315704-ffd4f701-bae8-4fa5-a56f-30a2b44b6e8b.png)
## Linebot畫面及註冊畫面:
![image](https://user-images.githubusercontent.com/58453878/131315642-7fe649e6-5289-474a-8408-c43356065ea6.png)
![image](https://user-images.githubusercontent.com/58453878/131315650-df6ed21d-2120-4ede-afe0-9cec44d891bf.png)
### 資料庫的建置、連結及資料庫導入API撰寫
資料庫架構:
![image](https://user-images.githubusercontent.com/58453878/131316076-862a7d6b-0dd6-4197-9ace-52abae163fc1.png)
1. 製作參照圖表了解表格屬性
2. 建立各個表格關聯性
3. 正則化表格建立
4. 利用MySQL控制收銀流程 
(更好的方式應該採用Redis 可以讓整體速度更快 這也是未來該更改的部份)
5. 撰寫API供他人快速導入 //程式碼詳情可參考(linebot/Flask/model/select.py)
### 資料產品爬蟲及資料清洗
Kaggle上只有產品編號,故我們將透過Kaggle提供的分類資訊來爬取相對應的產品,我們主要爬取的網站為:Amazon,Target,costco
* 資料爬取流程:
![image](https://user-images.githubusercontent.com/58453878/131319704-d49a5931-4f65-4c7b-93f1-5ddc6850ffa4.png)
1. 爬取Amazon資料時有遇到網站阻擋ip , 故我採取使用多IP的方式在每次爬取資料時隨機變更ip使網站不再阻擋  
//詳情程式碼請參考:爬蟲/ETL_amazon_search.py  
![image](https://user-images.githubusercontent.com/58453878/131321875-24e1c872-b169-4763-84ac-6f85a9ab7c4c.png)
2. 透過多線程的方式爬取網站 加速網站速度 //詳情程式碼請參考:爬蟲/target.com_說明.ipynb
* 資料清洗: //詳情程式碼:./sql_data_add.ipynb
1. 在Amazon爬取的資料評論數有遺漏值 故我將將數值型遺漏值做補值 透過範圍群組做平均值的方式
2. 清除網站爬取下來的特殊符號
3. cosco資料為台灣幣值 故將幣值轉換為美金
4. 整體清除重複值,再透過Amazon補剩下的缺值  
最終商品品項為:91,873  
![image](https://user-images.githubusercontent.com/58453878/131321085-22489681-bb47-418e-a48a-5322f00147a8.png)
### 口罩 / 人臉辨識系統
1. 口罩辨識系統: //程式碼參考 ./opencv/mask/
* 先利用RetinaFace套件追蹤人臉,只針對臉部的部分做偵測,並且減少環境影響值
* 口罩辨識模型利用CNN模型訓練 (用YOLO訓練也可以 但需求上利用CNN即可辦到 故使用CNN來辨識)
* 準確度與損失值:
![image](https://user-images.githubusercontent.com/58453878/131346809-00b798f0-2668-4d4f-a489-76c8e6926e63.png)
實際執行畫面:
![image](https://user-images.githubusercontent.com/58453878/131347066-d249df17-2dbd-4e7c-ae84-086d2c34791f.png)
2. 人臉辨識系統 //程式碼參考 ./opencv/Face
* 人臉辨識系統流程:
![image](https://user-images.githubusercontent.com/58453878/131347506-6eae10e0-9a81-4205-948b-a927f00c8275.png)
* 因我們要求顧客只提供一張相片故我們使用資料擴增的方式並隨機讓照片做翻轉,顛倒等 讓模型有更多資料可以訓練
* 使用Google開發的facenet深度學習模型, 取出臉部的128個特徵值
* 皆者使用SVM模型進行顧客分類辨識 , 並且利用K折交叉驗證器驗證準確度 因為每次新顧客都會產生一個新的模型故採用重複驗證準確度方式  
![image](https://user-images.githubusercontent.com/58453878/131349921-affca109-03b0-434f-9842-eeeca2f4c98d.png)

實際運作畫面:  
![image](https://user-images.githubusercontent.com/58453878/131350076-de53bc24-feaa-4e42-a0d9-c34ebfed03c4.png)

3. 自動化流程:  
加入Kafka接收來自linebot顧客的資訊 , 只要有新顧客就會執行建模 如果很多位顧客會以10個顧客為單位建模,建模完成後 攝影機會在每次閒置時檢查是否有新的模型
有新的模型會再重啟一次辨識系統 已達到自動化的功能  
![image](https://user-images.githubusercontent.com/58453878/131349075-4468057a-d001-4192-a3ad-a89e4b601298.png)
//完整程式碼請參考: ./opencv/Face/face_and_mask.py

### 警報系統
1. 無人商店針對程式無預警出錯時,需將錯誤紀錄,並在隨時能發送給工程師搶修
![image](https://user-images.githubusercontent.com/58453878/131349688-f043eb15-8d31-4a4e-bcb5-34fe0aca8989.png)

資料來源:  
* Kaggle消費資料:https://www.kaggle.com/frtgnn/dunnhumby-the-complete-journey
* Kaggle口罩照片:https://www.kaggle.com/vijaykumar1799/face-mask-detection
* YOLO口罩訓練資料:https://www.kaggle.com/andrewmvd/face-mask-detection

爬蟲資訊:  
* Amazon:https://www.amazon.com/
* target:https://www.target.com/
* costco:https://www.costco.com.tw/ 




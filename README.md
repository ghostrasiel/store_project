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
Kaggle上只有產品編號,故我們將透過Kaggle提供的分類資訊來爬取相對應的產品,我們主要爬取的網站為:Amazon,Target,cosco
* 資料爬取流程:
![image](https://user-images.githubusercontent.com/58453878/131319704-d49a5931-4f65-4c7b-93f1-5ddc6850ffa4.png)
1. 爬取Amazon資料時有遇到網站阻擋ip , 故我採取使用多IP的方式在每次爬取資料時隨機變更ip使網站不再阻擋 //詳情程式碼請參考:爬蟲/ETL_amazon_search.py  
![image](https://user-images.githubusercontent.com/58453878/131321875-24e1c872-b169-4763-84ac-6f85a9ab7c4c.png)
2. 透過多線程的方式爬取網站 加速網站速度 //詳情程式碼請參考:爬蟲/target.com_說明.ipynb
* 資料清洗: //詳情程式碼:./sql_data_add.ipynb
1. 在Amazon爬取的資料評論數有遺漏值 故我將將數值型遺漏值做補值 透過範圍群組做平均值的方式
2. 清除網站爬取下來的特殊符號
3. cosco資料為台灣幣值 故將幣值轉換為美金
4. 整體清除重複值,再透過Amazon補剩下的缺值  
最終商品品項為:91,873  
![image](https://user-images.githubusercontent.com/58453878/131321085-22489681-bb47-418e-a48a-5322f00147a8.png)





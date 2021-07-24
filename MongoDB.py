import csv
from pymongo import MongoClient
import atexit
from sshtunnel import SSHTunnelForwarder

server = SSHTunnelForwarder(('3.113.29.214', 22),
    ssh_password='koxhAS?ZRayMorAddS6*HzZMZ3LFh*wK',
    ssh_username='Administrator',
    remote_bind_address=('127.0.0.1', 27017))
server.start()

def shutdown():
    server.stop()

atexit.register(shutdown)

client = MongoClient('127.0.0.1', server.local_bind_port)

storedb = client.storedb #選擇操作的DataBase
# print(storedb)
collection = storedb.Amazon #選擇操作的Collection

# with open('Amazon_product.csv', newline='', encoding='utf-8-sig') as csvfile:
#     rows = csv.DictReader(csvfile)
#     for row in rows:
#         collection.insert_one(
#             row
#         )
#         print(row)
# print("資料寫入完成")

DataList=[]
for i in collection.find():
    DataList.append(i)
print(DataList)
client.close()
# con=1
# for i in collection.find(): 
#     with open("datatest1.csv", 'a', newline='',encoding='utf-8-sig') as csvfile:
#         columns_name = ["商品名稱","價格","商品說明","商品圖片","商品連結"]                  
#         writer = csv.DictWriter(csvfile,fieldnames=columns_name)
#         if con == 1:
#             writer.writeheader()
#             writer.writerow({"商品名稱":i['商品名稱'],"價格":i['價格'],"商品說明": i['商品說明'],"商品連結":i['商品連結'],"商品圖片":i['商品圖片'],"商品連結":i['商品連結']})
#         else:
#             writer.writerow({"商品名稱":i['商品名稱'],"價格":i['價格'],"商品說明": i['商品說明'],"商品連結":i['商品連結'],"商品圖片":i['商品圖片'],"商品連結":i['商品連結']})
#         con+=1
# print("已寫入{}筆資料".format(con))
import pymysql
import sys

host = '3.113.29.214'
user = 'eric'
passwd = '123456'
port = 3306
conninfo = {'host':host ,'port':port,'user':user , 'passwd': passwd, 'db':'store_db','charset':'utf8mb4'}

def add_product(values): #values = list(turple)
    try:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        add_product="""insert into product(product_id , name , price, commodity  , pz_url , description ,N_comments ,star_comments ) 
            values(%s , %s , %s , %s , %s , %s , %s  , %s );
            """
        cursor.executemany(add_product , values)
        conn.commit()
    except :
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()
    print("ok")

def select_product(select_list = ["product_id" , "name" , "price", "commodity"  , "pz_url" , "description" , "N_comments" , "star_comments" ] , where = None):
    data = None
    try:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        s = ','.join(select_list)
        if where == None :
            select = f"""select {s} from product ; """
        else:
            select = f"""select {s} from product where {where} ;"""

        cursor.execute(select)
        data = cursor.fetchall()

    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()

    return data




if __name__ == '__main__':
    #新增資料
    # values_truple = [(12345 , 'apple' , 1.99 , 'food' , 'https:' , 'this is apple' , 500 , 4.9 ),
    # (12346,'banane' , 2.99 , 'food'  , None , None , None , 3.9 )]
    # add_product(values_truple)

    # 查詢
    where = "product_id > 25671 and product_id <27000 limit 3"
    select_list = ['name' , 'price']
    for i in select_product(select_list=select_list , where=where):
        print(i)
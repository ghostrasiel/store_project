import pymysql
import datetime
import sys

conninfo = {'host':'3.113.29.214' , 'port':3306,'user':'eric' , 'passwd':'123456',
'db':'store_db','charset':'utf8mb4'}

def select_barsket(member_id):
    today = datetime.datetime.today()
    st_today = today.strftime('%Y-%m-%d')
    cash = 0
    word_list = []
    while True:
        try:
            conn = pymysql.connect(**conninfo)
            cursor = conn.cursor()
            select_product = f"""select b.member_id , p.name , b.quantity , round(p.price * b.quantity , 2) as 'Total'  , b.date
                from barsket as b natural join product as p where member_id ="{member_id}" and transaction_id is not null 
                and date >= (select date_format(date , '%Y-%m-%d') as date FROM store_db.barsket where member_id LIKE "{member_id}" and transaction_id  is not null group by date  order by date desc limit 1) ;  """

            cursor.execute(select_product)
            barsket_product = cursor.fetchall()
            for b in barsket_product:
                if b[2] != 0:
                    word_list.append(f'{b[1]},共{b[2]}樣')
                    cash += b[3]
                    user_id = b[0]
                    date = b[4]
            words = '\n'.join(word_list)
            break
        except:
            print('異常')
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
        finally:
            cursor.close()
            conn.close()

    if len(barsket_product) != 0:
        total = int(round(cash * 30, 0))
        return f'上次購買時間:\n{date}\n此次購買商品為:\n{words}\n總計消費金額: NT${total}'
    else:
        return '目前並無任何消費紀錄'


def edit_barsket(member_id , product_id):
    while True:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        break
    select_tag = f"""select tag from member_db where member_id LIKE '{member_id}'; """
    cursor.execute(select_tag)
    tag = cursor.fetchall()
    if len(tag) != 0 :
        select_product = f"""select count(*)  from barsket where (member_id = '{member_id}') and (product_id = {product_id})"""
        cursor.execute(select_product)
        count = cursor.fetchall()
        if tag[0][0] == 1:
            try:
                if count[0][0] >= 1 :
                    update = f"""update barsket set quantity = quantity + 1 where (member_id = '{member_id}') and (product_id = '{product_id}')  ;"""
                    cursor.execute(update)
                    conn.commit()
                elif count[0][0] == 0:
                    add =f'''insert into barsket(member_id , product_id ,quantity) 
                    values('{member_id}' , '{product_id}' , 1)'''
                    cursor.execute(add)
                    conn.commit() #完成交易
                text = '成功加入購物車'
            except:
                text = '無此項商品'
        elif tag[0][0] == 2:
            try:
                if count[0][0] >= 1 :
                    del_product = f"""delete FROM barsket WHERE (member_id = '{member_id}') and (product_id = '{product_id}')  ; """
                    cursor.execute(del_product)
                    conn.commit()
                    text = '成功移除購物車'
                elif count[0][0] == 0:
                    text = '購物車無此項商品'
            except:
                text = '無此項商品'

        elif tag[0][0] == 0 :
            text = '請點選要加入或移除商品'
    elif len(tag) == 0 :
        text = '請先加入會員'

    cursor.close()
    conn.close()
    return text

def add_member(html , member_id ):
    while True:
        try:
            conn = pymysql.connect(**conninfo)
            cursor = conn.cursor()
            break
        except:
            print('連線異樣')
    select = f'''select member_id from member_db where member_id = '{member_id}' ;'''
    cursor.execute(select)
    ms = cursor.fetchall()
    if len(ms) == 0 :
        text = f'{html}?user={member_id}'
    else:
        text = '你已經加入成功'
    
    cursor.close()
    conn.close()
    return text

def updata_tag(member_id , mesage) :
    while True:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        break
    select = f'''select member_id from member_db where member_id = '{member_id}' ;'''
    cursor.execute(select)
    ms = cursor.fetchall()
    if len(ms) == 1 :
        if mesage == '加入商品':
            update =f"""update member_db set tag = 1 where member_id Like '{member_id}' ;"""
            cursor.execute(update)
            conn.commit() #完成交易
            text = '請掃描要加入商品的Qrcode'
        elif mesage == '移除購物車商品':
            update =f"""update member_db set tag = 2 where member_id Like '{member_id}' ;"""
            cursor.execute(update)
            conn.commit() #完成交易
            text = '請掃描要移除購物車的商品Qrcode'
    else:
        text = '請先加入會員'
    
    cursor.close()
    conn.close()
    return text

def select_recommend(member_id) :
    while True:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        break
    try:
        select = f'''select member_id from select_recommend where member_id = '{member_id}' ;'''
        cursor.execute(select)
        text = cursor.fetchall()
    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()
    if len(text) != 0:
        return text
    else:
        return None

def add_select_recommend(member_id) :
    while True:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        break
    try:
        add_recommend = f'''insert into select_recommend(member_id) values('{member_id}') ;'''
        cursor.execute(add_recommend)
        conn.commit()
        print('ok')
    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()

def del_select_recommend(member_id) :
    while True:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        break
    try:
        del_recommend = f'''delete from select_recommend where member_id = '{member_id}' ;'''
        cursor.execute(del_recommend)
        conn.commit()
        print('ok')
    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()


    

# member_id = 'A_123458' #系統建立
# product_id = 111113 #輸入的商品

# #透過Line的對話傳送指令
# mesage = '查詢購物車'


# #購物車系統:
# #計算總金額 ###查詢目前有什麼
# if (mesage == '查詢購物車') or (mesage == "計算總金額" ):
#     print(select_barsket(member_id , mesage))
    
# #加入商品
# if mesage == '編輯購物車':
#     print(edit_barsket(member_id , product_id))

# #加入會員
# if mesage == '加入會員':
#     print(add_member(member_id))

# if (mesage == '移除購物車') or (mesage == "加入商品" ):
#     print(updata_tag(member_id , mesage))

if __name__ == '__main__':
    # today = datetime.datetime.today()
    # print(today.strftime('%Y-%m-%d'))
    add_select_recommend('U6ff9124eb8c4224f8fc607bd5e87ea29')
    print(select_recommend('U6ff9124eb8c4224f8fc607bd5e87ea29'))
    del_select_recommend('U6ff9124eb8c4224f8fc607bd5e87ea29')
    print(select_recommend('U6ff9124eb8c4224f8fc607bd5e87ea29'))

    # print(add_member('1234.com/' ,  member_id='U7216736aff9e39ca18b1534e6efe97bc'))
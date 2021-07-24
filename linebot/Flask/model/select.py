import pymysql

conninfo = {'host':'localhost' , 'port':3306,'user':'eric' , 'passwd':'123456',
'db':'store_db','charset':'utf8mb4'}

def select_barsket(member_id , text):
    while True:
        try:
            conn = pymysql.connect(**conninfo)
            cursor = conn.cursor()
            select_product =f"""select p.name ,b.quantity , round(p.price * b.quantity , 2) as 'Total' 
            from barsket as b natural join product as p where member_id LIKE "{member_id}" ;  """

            select_Total = f"""select sum(round(p.price * b.quantity , 2)) as 'basket_Total' 
            from barsket as b natural join product as p where member_id = "{member_id}" ; """
            cursor.execute(select_product)
            barsket_product = cursor.fetchall()
            cursor.execute(select_Total)
            barsket_Total = cursor.fetchall()
            word_list = [f'{b[0]},共{b[1]}樣' for b in barsket_product if b[1] != 0 ]
            words ='\n'.join(word_list)
            break
        except:
            print('連線異樣')
    cursor.close()
    conn.close()

    if barsket_Total[0][0] != None:
        if text == '查詢購物車':
            return f'你目前購物車有:\n{words}\n目前總計: ${barsket_Total[0][0]}'
        else :
            return f'目前你的購物金額為: ${barsket_Total[0][0]}'
    else:
        return '你目前購物車內無任何商品,請拍攝Qrcode加入商品' 


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

def add_member(member_id , name):
    while True:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        break
    select = f'''select member_id from member_db where member_id = '{member_id}' ;'''
    cursor.execute(select)
    ms = cursor.fetchall()
    if len(ms) == 0 :
        add =f'''insert into member_db(member_id) 
        values('{member_id}');'''
        cursor.execute(add)
        conn.commit() #完成交易
        text = f'Hi {name},歡迎你加入'
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
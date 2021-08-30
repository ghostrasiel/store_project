import pymysql
import sys
import datetime
import uuid



host = '3.113.29.214'
user = 'eric'
passwd = '123456'
port = 3306
conninfo = {'host':host ,'port':port,'user':user , 'passwd': passwd, 'db':'store_db','charset':'utf8mb4'}

def exit_register(register_id):
    now = datetime.datetime.today()
    st_today = now.strftime('%Y-%m-%d')
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    barsket_data = None
    transaction_id = f"b`{uuid.uuid1()}`"
    print(transaction_id)
    try:
        conn = pymysql.connect(**conninfo)
        cursor = conn.cursor()
        barsket_data , user_id , cash = select_barsket(register_id=register_id)
        update_reg = f"update cash_register set date= '{now}' , user = 'None' where id = '{register_id}' ; "
        cursor.execute(update_reg)
        if barsket_data != 'None' :
            insert_transaction = f"insert into transaction(transaction_id , date , sales_value ) values('{transaction_id}' , '{now}' , {float(cash)} )"
            cursor.execute(insert_transaction)
            update_barsket = f"update barsket set transaction_id = '{transaction_id}'  where member_id = '{user_id}' and date LIKE '{st_today}%' and transaction_id is null "
            cursor.execute(update_barsket)
            line_bot_push(barsket_data, user_id)

        conn.commit()
        print('ok')
    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
    finally:
        cursor.close()
        conn.close()

    if  barsket_data != 'None':
        return barsket_data , user_id
    else:
        return 'None' , 'None'

def select_barsket(register_id):
    today = datetime.datetime.today()
    st_today = today.strftime('%Y-%m-%d')
    cash = 0
    word_list = []
    while True:
        try:
            conn = pymysql.connect(**conninfo)
            cursor = conn.cursor()
            select_product = f"""select b.member_id , p.name , b.quantity , round(p.price * b.quantity , 2) as 'Total' 
            from barsket as b natural join product as p where member_id = (select user from cash_register where id = '{register_id}') and date LIKE "{st_today}%" and transaction_id is null ;  """

            cursor.execute(select_product)
            barsket_product = cursor.fetchall()
            for b in barsket_product:
                if b[2] != 0:
                    word_list.append(f'{b[1]},共{b[2]}樣')
                    cash += b[3]
                    user_id = b[0]
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
        return f'此次購買商品為:\n{words}\n總計支付金額: NT${total}\n謝謝惠顧!' , user_id , cash
    else:
        return 'None' , 'None' , 'None'

def line_bot_push(barsket_data , user_id):
    line_bot_api = LineBotApi('DHBv5Gy/320gHbddviD0q0R8AKg3iT1QPxLbaJBnNXEHceTDZm3BIjJuXfOKfUeJg6qu1Y+ONPHxeqs2W9d80M0+DXLIVDGo0tyDCzs7BJOFVxudtinckPAZH3fjeiXvQLzKI+8/Sy3I06VcLqG0LAdB04t89/1O/w1cDnyilFU=')
    user_ID = user_id
    # 主動推播的訊息
    line_bot_api.push_message(user_ID , TextSendMessage(text=barsket_data))


if __name__ == '__main__':
    barsket , uesr_id = exit_register('A')
    print(barsket)
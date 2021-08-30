import requests
import datetime
import sys
import pymysql

conninfo = {'host':'3.113.29.214' , 'port':3306,'user':'eric' , 'passwd':'123456',
'db':'store_db','charset':'utf8mb4'}
token = 'YJKTlrrWH9GOxoXWNoqcvrRudfJVwu4ktJuh8nyNIVV'

def add_logs(tag , log):
    now = datetime.datetime.today()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    while True:
        try:
            conn = pymysql.connect(**conninfo)
            cursor = conn.cursor()
            break
        except:
            print('連線異樣')
    try:
        add = f'''insert into system_logs(tag ,date , log ) 
                        values('{tag}' , '{now}' , '{log}');'''
        cursor.execute(add)
        conn.commit()
        print('ok')
    except:
        print('異常')
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        lineNotifyMessage(tag='mysql異常傳送' , msg=f'{sys.exc_info()[0]}\n{sys.exc_info()[1]}')
    finally:
        cursor.close()
        conn.close()

def lineNotifyMessage(tag , msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': f'起床加班！\n【{tag}】\n{msg}' }
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

def err_line_push(tag , msg=f'{sys.exc_info()[0]}\n{sys.exc_info()[1]}'):
    add_logs(tag=tag , log=msg.replace("'" , ''))
    lineNotifyMessage(tag=tag, msg=msg)

if __name__ == "__main__":
    err_line_push(tag='測試',msg='測試')
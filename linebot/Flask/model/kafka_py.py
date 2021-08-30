import sys
import datetime
from confluent_kafka import Producer
import json

def error_cb(err):
    sys.stderr.write(f'Error: {err}')

def delivery_callback(err, msg):
    if err:
        sys.stderr.write(f'Message failed delivery: {err}\n')
    else:
        print(f'Message delivered to topic: {msg.topic()} , parttion:{msg.partition()} , offset:{msg.offset()}')

def kafka_member(key , data):
    props = {
        # Kafka 集群在那裡?
        'bootstrap.servers': '3.112.128.223:9092',  # <-- 置換成要連接的 Kafka 集群
        'error_cb': error_cb  # 設定接收 error 訊息的 callback 函數
    }

    producer = Producer(props)
    topicName = 'store.member_add'
    json_data = json.dumps(data)
    try:
        print('Start sending messages ...')
        producer.produce(topicName,
                         key=str(key),
                         value=json_data ,
                         callback=delivery_callback )

    except BufferError as e:
        # 錯誤處理
        sys.stderr.write(
            f'Local producer queue is full ({len(producer)} messages awaiting delivery): try again\n'
        )

    except Exception as e:
        sys.stderr.write(str(e))

    producer.flush(10)
    print('Message sending completed!')


# 主程式進入點
if __name__ == '__main__':
    now = datetime.datetime.today()
    data = {'time': str(now), 'ip': '127.0.0.1', 'user_id': 'uu1234567', 'name': 'eric', 'age': 15, 'MARITAL': 'unknow',
            'INCOME': 'www', 'HH_COMP': '15K',
            'photo_url': 'https:ppp:ppp'}
    kafka_member('add_member' , data )


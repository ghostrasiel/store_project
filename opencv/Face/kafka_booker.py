import os
import sys
from confluent_kafka import Consumer, KafkaException, KafkaError
import json
from model import request_face , mysql , Alarm_system
import requests
import cv2
import pypinyin
import re

# Global Scope
offsets_dict = {}
records_pulled = True

# 用來接收從 Consumer instance 發出的 error 訊息
def error_cb(err):
    sys.stderr.write(f'Error: {err}')

# 轉換 msg_key 或 msg_value 成為 utf-8 的字串
def try_decode_utf8(data):
    return data.decode('utf-8') if data else None

# 當發生 Re-balance 時, 如果有 partition 被 assign 時被呼叫
def print_assignment(consumer, partitions):
    result = '[{}]'.format(
        ','.join([f'{p.topic}-{p.partition}' for p in partitions])
    )
    print(f'Setting newly assigned partitions: {result}')


# 當 Re-balance 被觸發後, Commit 現在 process 的 offsets
def commit_on_revoke(consumer, partitions):
    global offsets_dict
    for k, v in offsets_dict.items():
        consumer.commit(v)  # 進行異步的 commit

    result = '[{}]'.format(
        ','.join([f'{p.topic}-{p.partition}' for p in partitions])
    )

    print(f'Revoking previously assigned partitions: {result}')


# 當發生 commit 時被呼叫
def print_commit_result(err, partitions):
    if err:
        print(f'Failed to commit offsets: {err}: {partitions}')
    else:
        for p in partitions:
            print(f'Committed offsets for: {p.topic}-{p.partition} [offset={p.offset}]')
        try:
            face_model = request_face.face_model_py()
            face_model.build_model()
            print('face_modle重建成功')
        except:
            Alarm_system.err_line_push('建立人臉模型', msg=f'{sys.exc_info()[0]}\n{sys.exc_info()[1]}')


def add_member_sql(value):
    data = json.loads(value)
    print(data)
    print(data['time'] ,data['ip'])
    member_id = data['user_id']
    name = data['name']
    if re.search('[A-Z|a-z]', name) == None:
        result1 = pypinyin.pinyin(name, style=pypinyin.NORMAL)
        li = [result1[i][0] for i in range(len(result1))]
        name = ' '.join(li)

    dirPath = f'{os.getcwd()}\\data\\'
    picture_path = dirPath + name + '\\' + f'{name}.jpg'
    res = requests.get(url=data['photo_url'])

    if os.path.isfile(dirPath + name):
        pass
    else:
        os.mkdir(dirPath + name)

    with open(picture_path, 'wb') as f:
        f.write(res.content)

    face_model = request_face.face_model_py()
    img = cv2.imread(picture_path)
    face_list = face_model.check_face(img)

    if face_list != None:
        face_array1 = face_model.facenet_one_photo(img)
        # 轉換成二進制
        arr = face_array1.tostring()
        values = [(member_id, name, data['age'], data['MARITAL'] ,data['INCOME'] ,  data['HH_COMP'] ,arr, picture_path)]
        # print(values)
        mysql.add_member(values)
    else:
        print('無法辨識該照片')

if __name__ == '__main__':
    # 步驟1.設定要連線到 Kafka 集群的相關設定
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    props = {
        'bootstrap.servers': '3.112.128.223:9092',        # Kafka 集群在那裡? (置換成要連接的 Kafka 集群)
        'group.id': 'member',                            # ConsumerGroup 的名稱(置換成你/妳的學員 ID)
        'auto.offset.reset': 'earliest',              # 是否從這個 ConsumerGroup 尚未讀取的 partition/offset 開始讀
        'enable.auto.commit': False,                  # 是否啟動自動 commit
        'on_commit': print_commit_result,             # 設定接收 commit 訊息的 callback 函數
        'error_cb': error_cb                          # 設定接收 error 訊息的 callback 函數
    }

    # 步驟2. 產生一個 Kafka 的 Consumer 的實例
    consumer = Consumer(props)

    # 步驟3. 指定想要訂閱訊息的 topic 名稱
    topicName = 'store.member_add'

    # 步驟4. 讓 Consumer 向Kafka 集群訂閱指定的 topic
    consumer.subscribe([topicName],
                       on_assign=print_assignment, on_revoke=commit_on_revoke)
    # on_revoke 失去partitions 前你要做什麼
    # on_assign 你重新載入時要做甚麼

    # 步驟5. 持續的拉取 Kafka 有進來的訊息
    try:
        while True:
            # 請求 Kafka 把新的訊息吐出來
            records = consumer.consume(num_messages=10 , timeout=1.0)  # 批次讀取

            if not records:
                continue

            for record in records:
                if not record:
                    continue

                # 檢查是否有錯誤
                if record.error() and record.error().code() != KafkaError._PARTITION_EOF:
                    raise KafkaException(record.error())

                else:
                    records_pulled = True
                    # ** 在這裡進行商業邏輯與訊息處理 **

                    # 取出相關的 metadata
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    timestamp = record.timestamp()

                    # 取出 msg_key 與 msg_value
                    msg_key = try_decode_utf8(record.key())
                    msg_value = try_decode_utf8(record.value())

                    # 秀出 metadata 與 msg_key & msg_value 訊息
                    print('{}-{}-{} '.format(topic, partition, offset))
                    print('key:' , msg_key )
                    # print('value:' , msg_value)

                    add_member_sql(msg_value)

                    # 保留
                    offset_key = f"{topic}'|'{partition}"
                    offsets_dict[offset_key] = record  # 保留同一個 topic/partition 最後的 record

            # 異步地執行 commit (Async commit)
            if records_pulled:
                consumer.commit()
                offsets_dict.clear()  # 清除記錄

    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')

    except Exception as e:
        sys.stderr.write(str(e))

    finally:
        # 步驟6.關掉 Consumer 實例的連線
        consumer.close()
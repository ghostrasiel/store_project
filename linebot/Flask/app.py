from model import select , kafka_py , app_recom
from flask import Flask, request, abort , render_template , redirect , url_for
from werkzeug.utils import secure_filename
from linebot import LineBotApi, WebhookHandler 
from linebot.models import MessageEvent, TextSendMessage  , FlexSendMessage
from linebot.exceptions import InvalidSignatureError 
import os 
import re
import datetime

file = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__ , static_url_path='/assets',static_folder=f'{file}/assets')

# secretFile = json.load(open("secretFile.txt",'r'))
channelAccessToken = "DHBv5Gy/320gHbddviD0q0R8AKg3iT1QPxLbaJBnNXEHceTDZm3BIjJuXfOKfUeJg6qu1Y+ONPHxeqs2W9d80M0+DXLIVDGo0tyDCzs7BJOFVxudtinckPAZH3fjeiXvQLzKI+8/Sy3I06VcLqG0LAdB04t89/1O/w1cDnyilFU="
channelSecret = "92d9e21d2bc90fa86b15066acc52330b"

line_bot_api = LineBotApi(channelAccessToken)
handler = WebhookHandler(channelSecret)

@app.route('/')
def index():
    return 'hellos man'

@app.route('/member' , methods = ['GET' , 'POST'])
def member_html():
    url_host = request.host
    method = request.method
    userid = request.args.get('liff.state')
    ip = request.remote_addr
    if method == 'POST':
        name =request.form.get('name')
        age =request.form.get('age')
        MARITAL = request.form.get('MARITAL')
        INCOME = request.form.get('INCOME')
        HH_COMP = request.form.get('HH_COMP')
        f = request.files['file']
        fname = re.search('(jpg|png|jpeg|JPG|PNG|JPEG)' , secure_filename(f.filename)).group()
        upload_path = os.path.join(file, 'assets\\face_photo',f'{userid}.{fname}')
        print(upload_path)
        f.save(upload_path)

        photo_url = 'https://'+url_host + '/assets/face_photo/' + f'{userid}.{fname}'
        now = datetime.datetime.today()
        data = {'time': str(now),'ip':ip ,'user_id':str(userid),'name': name, 'age': age, 'MARITAL': MARITAL, 'INCOME': INCOME, 'HH_COMP': HH_COMP,
                'photo_url':  photo_url }
        print(data)
        # kafka_py.kafka_member('add_member', data)
        return redirect(url_for('welcome'))
    return render_template('/member.html')


@app.route('/welcome' )
def welcome():
    return render_template('/welcome.html')



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id) #取得個人資料
    member_id = profile.user_id
    print(member_id)
    if message_type =='image': #等待qrcode偵測
        pass

    elif message_type== 'text':
        name = profile.display_name #狀態消息
        mesage = event.message.text

        if (mesage == '上筆消費明細') : #查詢消費紀錄
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = select.select_barsket(member_id)))
        elif mesage == '加入會員': #加入會員
            # url_host = 'https://'+request.host
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=select.add_member(html='https://liff.line.me/1656184304-ZK3r5QbL', member_id=member_id)))


        elif mesage == "專屬推薦":
            FlexMessage = app_recom.recommend(user_id)
            if FlexMessage is None:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入商品名稱'))
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='專屬推薦你', contents=dict(FlexMessage)))
        elif mesage == "apple":
            FlexMessage = app_recom.recommendP(mesage)
            if FlexMessage is None:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text='查無相關商品'))
            else:
                line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='專屬推薦你', contents=dict(FlexMessage)))
        else:
            pass




        # elif mesage in ['111111' , '111112' , '111113']: #加入商品 暫時用數字替代
        #     product_id = int(event.message.text)
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text = select.edit_barsket(member_id , product_id)))
        # elif (mesage == '移除購物車商品') or (mesage == "加入商品" ): #編輯購物車
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text = select.updata_tag(member_id , mesage) ))


if __name__ == "__main__":
    app.run(host='0.0.0.0' , debug=True , port=80)
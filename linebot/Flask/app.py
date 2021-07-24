from model import select
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler 
from linebot.models import MessageEvent, TextMessage, TextSendMessage , ImageSendMessage 
from linebot.exceptions import InvalidSignatureError 
import os 
import re

file = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

# secretFile = json.load(open("secretFile.txt",'r'))
channelAccessToken = "DHBv5Gy/320gHbddviD0q0R8AKg3iT1QPxLbaJBnNXEHceTDZm3BIjJuXfOKfUeJg6qu1Y+ONPHxeqs2W9d80M0+DXLIVDGo0tyDCzs7BJOFVxudtinckPAZH3fjeiXvQLzKI+8/Sy3I06VcLqG0LAdB04t89/1O/w1cDnyilFU="
channelSecret = "92d9e21d2bc90fa86b15066acc52330b"

line_bot_api = LineBotApi(channelAccessToken)
handler = WebhookHandler(channelSecret)

@app.route('/')
def index():
    return 'hellos man'

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

        if (mesage == '查詢購物車') or (mesage == "計算總金額" ): #計算總金額 ###查詢目前有什麼
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = select.select_barsket(member_id , mesage)))
        elif mesage in ['111111' , '111112' , '111113']: #加入商品 暫時用數字替代
            product_id = int(event.message.text)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = select.edit_barsket(member_id , product_id)))
        elif mesage == '加入會員': #加入會員
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = select.add_member(member_id , name) ))
        elif (mesage == '移除購物車商品') or (mesage == "加入商品" ): #編輯購物車
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text = select.updata_tag(member_id , mesage) ))

if __name__ == "__main__":
    app.run(host='0.0.0.0' , debug=True)
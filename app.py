#載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import mongodb
import re

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('0CPr8hxcyyP0tJ6IR5RCZwF4JC/jufqCqJ6lZXbuhco4voDQ+gXutttuyJ6Y5a8ng39gLyd5U98VYFCd4M+G+UoX05r3+Zb+rODcj7asduAO7G4Zzzu7vvw+12ngFDrxkbw0l174KAL6sayaDVKSagdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('a3503c651ec279247c95bf5d9710edf4')

line_bot_api.push_message('U6ffbcc28d171270c3b7ed1375c61f68e', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'

#訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ### 抓到顧客資料 ###
    profile = LINE_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id #使用者ID
    usespeak = str(event.message.text)
    if re.match('[0-9]{4}[<>][0-9]', usespeak):
        # 先判斷是否是使用者儲存的股票
        mongodb.write_user_stock_function(stock=usespeak[0:4], bs=usespeak[4:5], price=usespeak[5:])
        LINE_bot_api.push_message(uid, TextSendMessage(usespeak[0:4]+'已經儲存成功'))
        return 0

    elif re.match('刪除[0-9]{4}', usespeak):
        # 刪除存在資料庫裏面的股票
        mongodb.delete_user_stock_function(stock=usespeak[2:])
        LINE_bot_api.push_message(uid, TextSendMessage(usespeak+'已經刪除成功'))
        return 0

#主程式
import os
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)

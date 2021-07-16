#web app#建立伺服器
#flask, django#後者用來做網頁的伺服器 

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('HrkCIS+iuiSzNGkQJ9zjIwJ56yxNlF1La2AW4z/Q1J3g6XbvBpulk743//11/BtGb2oAwxmU3voLncO4oYFKkCtKAzvszO0djqHm7XqYNBqNDAQt2LtvzWlU9s7Fy5uanCvDQ3nsbvoKR4JtEOvz6QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bf0f381646f3d404a152033ce4cd6e7f')

#接收line傳來訊息的程式碼
@app.route("/callback", methods=['POST'])#如果有人貼網址執行該路徑，callback就是trigger，會執行以下程式碼
def callback():#返回的觸發時間
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):#處理訊息
    msg = event.message.text#使用者傳的訊息
    
    r = '聽不懂拉 先請我吃好吃的再說話'#預設要回覆的訊息
    if msg == '嗨':
        r = '想找我槓麻呢':
    elif '胖' in msg:
        r = '你才胖全家都胖！'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))#回覆什麼訊息


if __name__ == "__main__":#加條件，確保如果該檔案是直接被執行，我們才執行以上內容，而不是直接跑程式碼
    app.run()#main function

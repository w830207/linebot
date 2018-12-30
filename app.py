from flask import Flask, request, abort
import os
import sys
import gspread

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,TextMessage,
    PostbackEvent,TextSendMessage,
    ImageSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,ConfirmTemplate,CarouselTemplate,
    PostbackTemplateAction,MessageTemplateAction,URITemplateAction,
    CarouselColumn
)

app = Flask(__name__)

ACCESS_TOKEN= os.environ['ACCESS_TOKEN']
SECRET= os.environ['CHANNEL_SECRET']

# Channel Access Token
line_bot_api = LineBotApi(ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(SECRET)






@app.route("/")
def hello_world():
    return "hello world!"


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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	if event.message.text != "":
			message = TextSendMessage(text='嗨帥哥你好！輸入"喝茶"提供服務哦！')
			line_bot_api.reply_message(event.reply_token, message)
	if event.message.text == "喝茶":
            confirm_template_message = TemplateSendMessage(
                            alt_text='請問您是否成年？', 
                            template=ConfirmTemplate(
                            text='請問您是否成年？',
                            actions=[
#                                PostbackTemplateAction 點擊選項後，
#                                 除了文字會顯示在聊天室中，
#                                 還回傳data中的資料，可
#                                 此類透過 Postback event 處理。
                                PostbackTemplateAction(
                                    label='是', 
                                    text='是',
                                    data='year=1'
                                ),
                                PostbackTemplateAction(
                                    label='否', 
                                    text='否',
                                    data='year=0'
                                )
                            ]
			)
		)
            line_bot_api.reply_message( event.reply_token,confirm_template_message)
	if event.message.text == '是':
			message = TextSendMessage(text='請輸入服務地區 服務地區:北區 西屯區 中區')
			line_bot_api.reply_message(event.reply_token, message)
	if event.message.text == '西屯區':
			message = TextSendMessage(text='test1')
			line_bot_api.reply_message(event.reply_token, message)
	elif event.message.text == '中區':
			message = TextSendMessage(text='test2')
			line_bot_api.reply_message(event.reply_token, message)
	elif event.message.text == '北區':
			message = TextSendMessage(text='test3')
			line_bot_api.reply_message(event.reply_token, message)
	else:
			message = TextSendMessage(text='不好意思目前該地區不提供服務\n請輸入服務地區 服務地區:北區 西屯區 中區')
			line_bot_api.reply_message(event.reply_token, message)
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

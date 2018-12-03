from flask import Flask, request, abort
import os
import sys
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,TextMessage,
    TextSendMessage,
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

google_data_spi = 'https://spreadsheets.google.com/feeds/list/2PACX-1vT9QMEsG9a8Hc7QrzjD_oTR97-10KEfhMfdvamHTMsJWDrFbyKzEec_s0nUmAJBuuEQrw7UEVCxc5bP/od6/public/values?alt=json'




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
    message = TextSendMessage(text='55555')
    line_bot_api.reply_message(event.reply_token, message)
    if event.message.text == "喝茶":
        button_template_message =ButtonsTemplate(
                            title='Menu', 
                            text='Please select',
                            ratio="1.51:1",
                            image_size="cover",
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
    
    
    
    
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

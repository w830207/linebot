from flask import Flask, request, abort
import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

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
	dictY = {'西屯區': 3, '中區': 4, '北區': 5,'東區': 2, '南區': 2, '西區': 2, '北屯區': 2, '南屯區': 2, '太平區': 2, '大里區': 2, '龍井區': 2, '沙鹿區': 2, '梧棲區': 2,'清水區': 2,'大甲區': 2,'霧峰區': 2, '烏日區': 2, '豐原區': 2,'后里區': 2, '石岡區': 2, '東勢區': 2, '和平區': 2, '新社區': 2, '潭子區': 2, '大雅區': 2, '神岡區': 2, '大雅區': 2, '大肚區': 2,'外埔區': 2,'大安區': 2}
	if event.message.text not in dictY and event.message.text != "是" and event.message.text != "喝茶":
			message = TextSendMessage(text='嗨帥哥你好！輸入"喝茶"提供服務哦！\n目前只有台中地區提供服務')
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
	elif event.message.text == "是":
			message = TextSendMessage(text='請輸入服務地區 服務地區:北區 西屯區 中區')
			line_bot_api.reply_message(event.reply_token, message)
	elif dictY[event.message.text]==3:
			#'西屯區': 3, '中區': 4, '北區': 5
			#GDriveJSON就輸入下載下來Json檔名稱
			#GSpreadSheet是google試算表名稱
			GDriveJSON = 'teafish-75f3bc4ebb90.json'
			GSpreadSheet = 'teafish'
			while True:
				try:
					scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
					key = SAC.from_json_keyfile_name(GDriveJSON, scope)
					gc = gspread.authorize(key)
					worksheet = gc.open(GSpreadSheet).worksheet("中區")
				except Exception as ex:
					print('無法連線Google試算表', ex)
					sys.exit(1)
				cell_list4 = worksheet.range('A4:E4')
				if cell_list4 !="":
					ttt = str(cell_list4)
					for i in range(8,21):
						if worksheet.cell(4, i).value =="" :
							ttt += ' '+str(i+4)+'available'
					message4 = TextSendMessage(text=ttt)
					break
				cell_list5 = worksheet.range('A5:E5')
				if cell_list5 !="":
					ttt = str(cell_list5)
					for i in range(8,21):
						if worksheet.cell(5, i).value =="" :
							ttt += ' '+str(i+4)+'available'
					message5 = TextSendMessage(text=ttt)
					break
			line_bot_api.reply_message(event.reply_token, message4)
			line_bot_api.reply_message(event.reply_token, message5)
	elif dictY[event.message.text]==5:
			#'西屯區': 3, '中區': 4, '北區': 5
			#GDriveJSON就輸入下載下來Json檔名稱
			#GSpreadSheet是google試算表名稱
			GDriveJSON = 'teafish-75f3bc4ebb90.json'
			GSpreadSheet = 'teafish'
			while True:
				try:
					scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
					key = SAC.from_json_keyfile_name(GDriveJSON, scope)
					gc = gspread.authorize(key)
					worksheet = gc.open(GSpreadSheet).worksheet("中區")
				except Exception as ex:
					print('無法連線Google試算表', ex)
					sys.exit(1)
				cell_list4 = worksheet.range('A4:E4')
				if cell_list4 !="":
					ttt = str(cell_list4)
					for i in range(8,21):
						if worksheet.cell(4, i).value =="" :
							ttt += ' '+str(i+4)+'available'
					message4 = TextSendMessage(text=ttt)
					break
				cell_list5 = worksheet.range('A5:E5')
				if cell_list5 !="":
					ttt = str(cell_list5)
					for i in range(8,21):
					#8-21代表營業時間從1200-2400
						if worksheet.cell(5, i).value =="" :
							ttt += ' '+str(i+4)+'available'
					message5 = TextSendMessage(text=ttt)
					break
			line_bot_api.reply_message(event.reply_token, message4)
			line_bot_api.reply_message(event.reply_token, message5)
	elif dictY[event.message.text]==4:
			#'西屯區': 3, '中區': 4, '北區': 5
			#GDriveJSON就輸入下載下來Json檔名稱
			#GSpreadSheet是google試算表名稱
			GDriveJSON = 'teafish-75f3bc4ebb90.json'
			GSpreadSheet = 'teafish'
			while True:
				try:
					scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
					key = SAC.from_json_keyfile_name(GDriveJSON, scope)
					gc = gspread.authorize(key)
					worksheet = gc.open(GSpreadSheet).worksheet("中區")
				except Exception as ex:
					print('無法連線Google試算表', ex)
					sys.exit(1)
				cell_list4 = worksheet.range('A4:E4')
				if cell_list4 !="":
					ttt = str(cell_list4)
					for i in range(8,21):
					#8-21代表營業時間從1200-2400
						if worksheet.cell(4, i).value =="" :
							ttt += ' '+str(i+4)+'available'
					message4 = TextSendMessage(text=ttt)
					break
				cell_list5 = worksheet.range('A5:E5')
				if cell_list5 !="":
					ttt = str(cell_list5)
					for i in range(8,21):
					#8-21代表營業時間從1200-2400
						if worksheet.cell(5, i).value =="" :
							ttt += ' '+str(i+4)+'available'
					message5 = TextSendMessage(text=ttt)
					breaktSendMessage(text=ttt)
					break
			line_bot_api.reply_message(event.reply_token, message4)
			line_bot_api.reply_message(event.reply_token, message5)
	elif dictY[event.message.text]==2:
			message = TextSendMessage(text='不好意思目前該地區不提供服務\n請輸入服務地區 服務地區:北區 西屯區 中區')
			line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

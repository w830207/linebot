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


def book(sht,loc):
	#GDriveJSON就輸入下載下來Json檔名稱
	#GSpreadSheet是google試算表名稱
	dict = {'西屯區': 1, '中區': 1, '北區': 1}
	GDriveJSON = 'teafish-75f3bc4ebb90.json'
	GSpreadSheet = 'teafish'
	while True:
		try:
			scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
			key = SAC.from_json_keyfile_name(GDriveJSON, scope)
			gc = gspread.authorize(key)
			worksheet = gc.open(GSpreadSheet).worksheet(sht)
		except Exception as ex:
			print('無法連線Google試算表', ex)
			sys.exit(1)
		if sht in dict and worksheet.acell(loc).value =="":
			worksheet.update_acell(loc, 'Bingo!')
			return("預約成功")
		elif worksheet.acell(loc).value !="":
			return("預約失敗請重新選擇地區或是小姐的服務時間")
		break


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	dictY = {'北區':1,'中區':1,'西屯區':1,'東區': 2, '南區': 2, '西區': 2, '北屯區': 2, '南屯區': 2, '太平區': 2, '大里區': 2, '龍井區': 2, '沙鹿區': 2, '梧棲區': 2,'清水區': 2,'大甲區': 2,'霧峰區': 2, '烏日區': 2, '豐原區': 2,'后里區': 2, '石岡區': 2, '東勢區': 2, '和平區': 2, '新社區': 2, '潭子區': 2, '大雅區': 2, '神岡區': 2, '大雅區': 2, '大肚區': 2,'外埔區': 2,'大安區': 2}
	dictW = {'appleW15': 'H4','appleW16': 'I4','appleW17': 'J4','appleW18': 'K4','appleW19': 'L4','appleW20': 'M4','appleW21': 'N4','appleW22': 'O4','appleW23': 'P4','appleW24': 'R4','bananaW15': 'H5','bananaW16': 'I5','bananaW17': 'J5','bananaW18': 'K5','bananaW19': 'L5','bananaW20': 'M5','bananaW21': 'N5','bananaW22': 'O5','bananaW32': 'P5','bananaW24': 'R5'}
	dictM = {'appleM15': 'H4','appleM16': 'I4','appleM17': 'J4','appleM18': 'K4','appleM19': 'L4','appleM20': 'M4','appleM21': 'N4','appleM22': 'O4','appleM32': 'P4','appleM24': 'R4','bananaM15': 'H5','bananaM16': 'I5','bananaM17': 'J5','bananaM18': 'K5','bananaM19': 'L5','bananaM20': 'M5','bananaM21': 'N5','bananaM22': 'O5','bananaM32': 'P5','bananaM24': 'R5'}
	dictN = {'appleN15': 'H4','appleN16': 'I4','appleN17': 'J4','appleN18': 'K4','appleN19': 'L4','appleN20': 'M4','appleN21': 'N4','appleN22': 'O4','appleN32': 'P4','appleN24': 'R4','bananaN15': 'H5','bananaN16': 'I5','bananaN17': 'J5','bananaN18': 'K5','bananaN19': 'L5','bananaN20': 'M5','bananaN21': 'N5','bananaN22': 'O5','bananaN32': 'P5','bananaN24': 'R5'}
	if event.message.text  in dictW:
			book("西屯區",dictW[event.message.text])
			message = TextSendMessage(text='預約成功')
			line_bot_api.reply_message(event.reply_token, message)
	elif event.message.text  in dictM:
			book("中區",dictM[event.message.text])
			message = TextSendMessage(text='預約成功')
			line_bot_api.reply_message(event.reply_token, message)
	elif event.message.text  in dictN:
			book("北區",dictN[event.message.text])
			message = TextSendMessage(text='預約成功')
			line_bot_api.reply_message(event.reply_token, message)
	if event.message.text not in dictY and event.message.text != "我已成年" and event.message.text != "喝茶":
			message = TextSendMessage(text='嗨帥哥你好！輸入"喝茶"提供服務哦！\n目前只有台中地區提供服務')
			line_bot_api.reply_message(event.reply_token, message)
	if event.message.text == "喝茶":
            message = TemplateSendMessage(
                            alt_text='請問您是否成年？', 
                            template=ConfirmTemplate(
                            text='請問您是否成年？',
                            actions=[
                                PostbackTemplateAction(
                                    label='是', 
                                    text='我已成年',
                                    data='year=1'
                                ),
                                PostbackTemplateAction(
                                    label='否', 
                                    text='我未成年',
                                    data='year=0'
                                )
                            ]
			)
		)
            line_bot_api.reply_message(event.reply_token, message)
	if event.message.text == "我已成年":
			message = TextSendMessage(text='請輸入服務地區 服務地區:北區 西屯區 中區')
			line_bot_api.reply_message(event.reply_token, message)
	compare_txt = ["西屯區", "西屯"]
	for x in compare_txt:
		if event.message.text.find(x) != -1:
			sht = "西屯區"
			GDriveJSON = 'teafish-75f3bc4ebb90.json'
			GSpreadSheet = 'teafish'
			scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
			key = SAC.from_json_keyfile_name(GDriveJSON, scope)
			gc = gspread.authorize(key)
			worksheet = gc.open(GSpreadSheet).worksheet(sht)
			ttt = ""
			for j in range(4,11):
				if worksheet.cell(j, 1).value !="" :
					pic = str(worksheet.cell(j, 6).value)
					for i in range(1,5):
						ttt += "\n"+str(worksheet.cell(j, i).value)
					for i in range(8,18):
						if worksheet.cell(5, i).value =="" :
							ttt += "\n"+str(i+7)+'available'
			ttt += '預約請回覆小姐名稱加時間 例如 吉澤明步16'
			message = (ImageSendMessage(original_content_url=pic,preview_image_url=pic),TextSendMessage(text=ttt))
			line_bot_api.reply_message(event.reply_token, message)
	if event.message.text.find(x) != -1:
			sht = "中區"
			GDriveJSON = 'teafish-75f3bc4ebb90.json'
			GSpreadSheet = 'teafish'
			scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
			key = SAC.from_json_keyfile_name(GDriveJSON, scope)
			gc = gspread.authorize(key)
			worksheet = gc.open(GSpreadSheet).worksheet(sht)
			ttt = ""
			for j in range(4,11):
				pic = str(worksheet.cell(j, 6).value)
				if worksheet.cell(j, 1).value !="" :
					for i in range(1,5):
						ttt += "\n"+str(worksheet.cell(j, i).value)
					for i in range(8,18):
						if worksheet.cell(5, i).value =="" :
							ttt += "\n"+str(i+7)+'available'
			ttt += '預約請回覆小姐名稱加時間 例如 吉澤明步16'
			message = (ImageSendMessage(original_content_url=pic,preview_image_url=pic),TextSendMessage(text=ttt))
			line_bot_api.reply_message(event.reply_token, message)
	if event.message.text.find(x) != -1:
			sht = "北區"
			GDriveJSON = 'teafish-75f3bc4ebb90.json'
			GSpreadSheet = 'teafish'
			scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
			key = SAC.from_json_keyfile_name(GDriveJSON, scope)
			gc = gspread.authorize(key)
			worksheet = gc.open(GSpreadSheet).worksheet(sht)
			ttt = ""
			for j in range(4,11):
				if worksheet.cell(j, 1).value !="" :
					pic = str(worksheet.cell(j, 6).value)
					for i in range(1,5):
						ttt += "\n"+str(worksheet.cell(j, i).value)+"\n"
					for i in range(8,18):
						if worksheet.cell(5, i).value =="" :
							ttt += "\n"+str(i+7)+'available'
			ttt += "\n預約請回覆小姐名稱加時間 例如 吉澤明步16"
			message = (ImageSendMessage(original_content_url=pic,preview_image_url=pic),TextSendMessage(text=ttt))
			line_bot_api.reply_message(event.reply_token, message)
	if dictY[event.message.text]==2:
			message = TextSendMessage(text='不好意思目前該地區不提供服務\n請輸入服務地區 服務地區:北區 西屯區 中區')
			line_bot_api.reply_message(event.reply_token, message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

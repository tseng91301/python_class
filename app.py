from flask import Flask, abort
from flask import render_template
from flask import request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os

import requests
import re
import json

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route('/testupl',methods=['GET'])
def testupl():
    sendcm_first_url="https://send.cm/upload"
    sendcm_first_response=requests.get(sendcm_first_url)
    if(sendcm_first_response.status_code==200):
        t1=sendcm_first_response.text
        pattern = r'https://[^/]+.send.cm/cgi-bin/upload.cgi\?[^\s]+(?=\")'
        upload_location=re.search(pattern,t1).group(0)
        #print(upload_location)
    else:
        print("Get upload location failed with status code [{sendcm_first_response.status_code}]")

    upl_form_data={
        "utype":"anon",
        "file_expire_unit":"DAY",
        "keepalive":1
    }

    response=requests.post(upload_location,data=upl_form_data,files={'file_0':open("test.txt",'rb')})
    #print(response.status_code)
    #print(response.text)

    file_id=json.loads(response.text)[0]['file_code']
    if(file_id=="undef"):
        print("Failed to upload file, remote banned")
        return "Upload failed..."

    sendcm_getlink_url="https://send.cm/?op=upload_result&st=OK&fn="+file_id
    t1=requests.get(sendcm_getlink_url).text
    dl_link=(re.search(r'(?<=height:5px">).*?(?=<\/textarea>)',t1)).group(0)
    return dl_link

@app.route('/testenv',methods=['GET'])
def testenv():
    # 设置环境变量
    os.environ["TEST_ENV"] = "FDSFJHDSJKFHJDSFHJS"

    # 读取一个特定的环境变量
    env_variable_value = os.getenv("TEST_ENV")

    # 如果环境变量不存在，你可以提供一个默认值
    env_variable_value = os.getenv("TEST_ENV", "DEFAULT_VALUE")

    return env_variable_value

@app.route('/helloname', methods=['GET'])
def helloname():
    if request.method == 'GET': 
        return 'Hello ' + request.values['username'] 

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
    msg = event.message.text
    try:
        if(os.getenv(event.source.user_id+"_mode")=="formpdf"):
            t1=formpdf(event.source.user_id,msg)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
            return
        elif(os.getenv(event.source.user_id+"_mode")=="python"):
            t1=python_exec(msg)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
        answer = '"'+msg+'", received!'
        #print(answer)
        if(msg=="help"):
            t1=open("help/helpmain.txt",'r').read()
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
        elif(msg=="upload test"):
            t1=testupl()
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
        elif(msg=="test env"):
            t1=testenv()
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
        elif(msg=="user"):
            t1 = event.source.user_id
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
        elif(msg=="form pdf"):
            t1=open("pdfcompose/mainmsg.txt",'r').read()
            os.environ[event.source.user_id+"_mode"] = "formpdf"
            os.environ[event.source.user_id+"_data"] = '{"test":"test"}'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
        elif(msg=="python"):
            t1="Entering Python coding mode\r\nYou can send Python script to the API to debug"
            os.environ[event.source.user_id+"_mode"] = "python"
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(answer))
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('An error occurred'))

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)

@app.route('/')
def hello():
    return 'Hello, World!'

def settxtdata(cli_id,title,information):
    return
def formpdf(cli_id,arg):
    data=json.loads(os.getenv(cli_id+"_data"))
    if(os.getenv(cli_id+"_mode2")=="topic1"):
        data['topic1']=arg
        os.environ[cli_id+"_mode2"] = ""
        os.environ[cli_id+"_data"]=json.dumps(data)
        return "complete topic1 insertion"
    
    if(arg=="exit"):
        os.environ[cli_id+"_mode"] = ""
        return "mode ended"
    if(arg=="dump"):
        return json.dumps(data)
    if(arg=="topic1"):
        os.environ[cli_id+"_mode2"] = "topic1"
        return "Setting topic 1 please type your topic 1 (exit topic1 after next input)"
    if(arg=="topic2"):
        os.environ[cli_id+"_mode2"] = "topic2"
        return "Setting topic 2 please type your topic 2 \n(send divided information, and type 'ok' to exit topic2)\n(enter the same text as the exist information to delete it)"
    return
def python_exec(command):
    try:
        output=exec(command)
    except:
        output="Command error!"
    return str(output)

if __name__ == '__main__':
    app.run()

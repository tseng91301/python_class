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

#from module import pdfgen

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
    python_trigger=['python','Python','Py','py']
    try:
        if(os.getenv(event.source.user_id+"_mode")=="formpdf"):
            t1=formpdf(event.source.user_id,msg)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
            return
        elif os.getenv(event.source.user_id+"_mode") in python_trigger:
            if(detect_exit(msg)):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("Exit Python command section"))
                os.environ[event.source.user_id+"_mode"] = ""
                return
            t1=python_exec(msg)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
        answer = '"'+msg+'", received!'
        #print(answer)
        if(re.match(r"(-){,2}[hH]{1}elp\s*",msg)):
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
        elif(re.match(r"[Ff]{1}orm(\s)*(pdf|PDF)",msg)):
            t1=open("pdfcompose/mainmsg.txt",'r').read()
            os.environ[event.source.user_id+"_mode"] = "formpdf"
            os.environ[event.source.user_id+"_data"] = json.dumps({"topic1":"","topic2":[],"topic3": {}})
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
        elif msg in python_trigger:
            t1="Entering Python coding mode\r\nYou can send Python script to the API to debug"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
            os.environ[event.source.user_id+"_mode"] = "python"
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(answer))
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('An error occurred: '+str(e)))

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
    if(os.getenv(cli_id+"_mode2")=="topic2"):
        if(os.getenv(cli_id+"_mode3")=="del"):
            t1=arg.split(',')
            t1=[int(ele) for ele in t1]
            data['topic2']=rmv(data['topic2'],t1)
            os.environ[cli_id+"_mode3"] = ""
            os.environ[cli_id+"_data"]=json.dumps(data)
            return "success!"

        if(arg=="ok"):
            os.environ[cli_id+"_mode2"] = ""
            return "exit topic2 insertion"
        elif(arg=="del"):
            out="Please type the number to del that column :\n"
            out+="to delete multiple data, type ',' between numbers\n"
            for i,v in enumerate(data['topic2']):
                out+=str(i)+": "+v+"\n"
            os.environ[cli_id+"_mode3"] = "del"
            return out
        
        tmp=arg.split('\n')
        data['topic2']=data['topic2']+tmp
        os.environ[cli_id+"_data"]=json.dumps(data)
        return "complete topic2 insertion, if complete insertion, type 'ok'"
    if(os.getenv(cli_id+"_mode2")=="topic3"):
        if(os.getenv(cli_id+"_mode3")=="del"):
            t1=arg.split(',')
            t1=[int(ele) for ele in t1]
            data['topic2']=rmv(data['topic2'],t1)
            os.environ[cli_id+"_mode3"] = ""
            os.environ[cli_id+"_data"]=json.dumps(data)
            return "success!"

        if(arg=="ok"):
            os.environ[cli_id+"_mode2"] = ""
            return "exit topic3 insertion"
        elif(arg=="del"):
            out="Please type the number to del that column :\n"
            out+="to delete multiple data, type ',' between numbers\n"
            for i,v in enumerate(data['topic3']):
                out+=str(i)+": "+v+": "+data['topic3'][v]+"\n"
            os.environ[cli_id+"_mode3"] = "del"
            return out
        tmp=arg.split('\n')
        tmp2={}
        for con in tmp:
            tmp3=re.split(r":(\s)*",con,1)
            tmp2[tmp3[0]]=tmp3[2]
        data['topic3'].update(tmp2)
        os.environ[cli_id+"_data"]=json.dumps(data)
        return "complete topic2 insertion, if complete insertion, type 'ok'"

    
    if(detect_exit(arg)):
        os.environ[cli_id+"_mode"] = ""
        return "mode ended"
    if(arg=="dump"):
        return json.dumps(data)
    if(arg=="topic1"):
        os.environ[cli_id+"_mode2"] = "topic1"
        return "Setting topic 1 please type your topic 1 (exit topic1 after input)"
    if(arg=="topic2"):
        os.environ[cli_id+"_mode2"] = "topic2"
        return "Setting topic 2\n please type your topic 2 \n(send divided information, and type 'ok' to exit topic2)"
    if(arg=="topic3"):
        os.environ[cli_id+"_mode2"] = "topic3"
        return "Setting topic 3\n please type your topic 3 \n(send divided information, and type 'ok' to exit topic2)"
    return
def python_exec(command):
    try:
        output=exec(command)
    except Exception as e:
        output=str(e)
    return str(output)

def rmv(inp,ele):
    tmpa=[]
    for i,v in enumerate(inp):
        if i not in ele:
            tmpa.append(v)
    return tmpa
def rmv2(inp,ele):
    tmpa={}
    for i,v in enumerate(inp):
        if i not in ele:
            tmpa.update({v:inp[v]})
    return tmpa


def detect_exit(inp):
    return(re.match(r"^[Ee]{1}xit[(\(\))]{0,1}[;]{0,1}$",inp))

if __name__ == '__main__':
    app.run()

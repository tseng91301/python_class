from flask import Flask, abort
from flask import render_template,make_response
from flask import request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import requests
from io import BytesIO
import re
import json
from datetime import datetime
import os

#from module import pdfgen
from env import getenv
from pdfcompose.create_md import tomd
from pdfcompose import template,form
from help.help import help,help_mode

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

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
    uid=event.source.user_id
    mode=getenv.get_mode(uid)
    try:
        print(str(mode))
        #Basic Operation, including go back, help and end mode
        if(detect_exit(msg)): #exit mode
            getenv.set_mode(uid,[])
            line_bot_api.reply_message(event.reply_token, TextSendMessage("mode ended"))
            return
        if(detect_back(msg)): #back to last mode
            if(len(mode)==1):
                t1="No specified step in "+mode[0]+", type 'Exit' to exit the mode"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
                return
            mode.pop()
            getenv.set_mode(uid,mode)
            if(len(mode)==1):
                t1="No specified step in "+mode[0]+", type 'Exit' to exit the mode"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
                return
            t1="You are at "
            for n,v in enumerate(mode):
                if(n!=0):
                    t1+=" -> "
                t1+=v
            t1+=" ."
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
            return
        if(detect_help(msg)): #show help message of the mode
            t1=help_mode(mode)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
            return
        
        #When receiving message when mode is formpdf
        try:
            if(str(mode[0])=="formpdf"):
                t1=formpdf(uid,msg)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
                return
        except Exception as e:
            print('at if(mode[0]=="formpdf"): , '+str(e))
        
        #Mode entrance, receiving message to enter the mode
        if(re.match(r"^[Ff]{1}orm(\s)*(pdf|PDF)$",msg)):
            mode=list(["formpdf"])
            getenv.set_mode(uid,mode)
            t1=help_mode(mode)
            getenv.set_data(uid,template.data_i())
            line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
            return
        
        #Others, if user type other commands when no mode specified
        t1="You type: "+msg+".\n\n"
        t1+=help()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(t1))
        return
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
    message = TextSendMessage(text=f'{name}, welcome to the Line server')
    line_bot_api.reply_message(event.reply_token, message)

@app.route('/')
def hello():
    return 'Hello, World!'
@app.route('/download', methods=['GET'])
def download():
    if request.method=='GET':
        op=int(request.values['op'])
        uid=request.values['uid']
        print(op)
        print(uid)
        print(getenv.download_permission(uid))
        if(getenv.download_permission(uid)==op):
            if(op==1): #Operation to download file
                response=make_response(str(getenv.get_data(uid)))
                response.headers['Content-Disposition'] = 'attachment; filename='+uid+'.json'
                response.status_code=200
                getenv.download_permission(uid,0)
                return response
        response=make_response("Abort!")
        response.status_code=403
        return response
    
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method=='GET':
        op=int(request.values['op'])
        uid=request.values['uid']
        print(op)
        print(uid)
        print(getenv.upload_permission(uid))
        if(getenv.upload_permission(uid)==op):
            if(op==1): #Operation to download file
                t1=open("upload_page/upl_1.html_p1").read()
                t2=open("upload_page/upl_1.html_p2").read()
                response=make_response(t1+uid+t2)
                response.status_code=200
                return response
    if request.method=='POST':
        print("POST")
    response=make_response("Abort!")
    response.status_code=403
    return response
            
@app.route('/helloname', methods=['GET'])
def helloname():
    if request.method == 'GET': 
        return 'Hello ' + request.values['username'] 



def upload_data(inp,v=1,ext="pdf",name=""):
    inp=str(inp)
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
    if(v): # Virtual file data
        
        # 定义虚拟文件内容
        file_content = inp.encode('utf-8')

        # 创建一个 BytesIO 对象，用于模拟文件对象
        virtual_file = BytesIO(file_content)

        response=requests.post(upload_location,data=upl_form_data,files={str(datetime.now())+'.'+str(ext):virtual_file})
    else:
        response=requests.post(upload_location,data=upl_form_data,files={'file_0':open(name,'rb')})
    file_id=json.loads(response.text)[0]['file_code']
    if(file_id=="undef"):
        #print("Failed to upload file, remote banned")
        return "error"

    sendcm_getlink_url="https://send.cm/?op=upload_result&st=OK&fn="+file_id
    t1=requests.get(sendcm_getlink_url).text
    dl_link=(re.search(r'(?<=height:5px">).*?(?=<\/textarea>)',t1)).group(0)
    return dl_link  

def formpdf(uid,arg):
    mode=getenv.get_mode(uid)
    try:
        data=getenv.get_data(uid)
    except Exception as e:
        print("At data=getenv.get_data(uid), "+str(e))
        data=template.data_i()
    
    # when not specified step
    if(len(mode)==1):
        # Do something to configuration file
        if(arg=="dump"):
            return json.dumps(data)
        elif arg in ["Config download","Config-d"]:
            t1="Please visit the following link to access your config file: \n\n"
            t1+="https://line-pdf-bot.onrender.com/download"+"?uid="+uid+"&op=1\n\n"
            t1+="Note: The link is just available just ONCE!"
            getenv.download_permission(uid,1)
            return t1
        elif arg in ["Config use","Config upload","Config-u"]:
            t1="Please visit the following link to upload your configuration file: \n\n"
            t1+="https://line-pdf-bot.onrender.com/upload"+"?uid="+uid+"&op=1\n\n"
            t1+="Note: The link is just available just ONCE!"
            getenv.upload_permission(uid,1)
            return t1
            
        elif(re.match(r"^[Ee]{1}xport\s*$",arg)):
            reply=upload_data(tomd(data),ext="md")
            if(reply=="error"):
                return "Upload error, maybe you upload too many times on the same content"
            return "Click the link to reach the file: "+reply
        if arg in ["Basic","B","basic"]:
            mode=[mode[0],"basic"]
            getenv.set_mode(uid,mode)
            return help_mode(mode)
        if arg in ["Education","Edu"]:
            mode=[mode[0],"education"]
            getenv.set_mode(uid,mode)
            return help_mode(mode)
        if arg in ["Professional","Professional experience","Prof"]:
            mode=[mode[0],"professional"]
            getenv.set_mode(uid,mode)
            return help_mode(mode)
        if arg in ["Leadership","Lead"]:
            mode=[mode[0],"leadership"]
            getenv.set_mode(uid,mode)
            return help_mode(mode)
        if arg in ["Certification","Cert"]:
            mode=[mode[0],"certification"]
            getenv.set_mode(uid,mode)
            return help_mode(mode)
        if arg in ["Skill","Skills"]:
            mode=[mode[0],"skill"]
            getenv.set_mode(uid,mode)
            return help_mode(mode)
        if arg in ["Additional","Plus"]:
            mode=[mode[0],"additional"]
            getenv.set_mode(uid,mode)
            return help_mode(mode)
        
        return "Unknown command '"+arg+"' !"
    
    # when specified step
    t1=form.detail(mode,data,arg)
    if(t1["success"]):
        mode=t1["mode"]
        data=t1["data"]
        if(t1["msg"]!=""):
            ret=t1["msg"]
        elif(t1["help"]):
            ret=help_mode(mode,2)
        else:
            ret="Operation successful"
    else:
        ret="Error: \n"+t1["error"]
    getenv.set_mode(uid,mode)
    getenv.set_data(uid,data)
    return ret

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

def check_exist(data:list,inp:list):
    find=0
    try:
        for n1,d1 in enumerate(data):
            if(n1==len(data)-1):
                break
            find1=1
            for n2,d2 in enumerate(inp):
                if(data[n1+n2]!=inp[n2]):
                    find1=0
                    break
            if(find1):
                find=1
                break
    except:
        find=0
    return bool(find)



def detect_exit(inp):
    return(bool(re.match(r"^[Ee]{1}xit[(\(\))]{0,1}[;]{0,1}$",inp)))

def detect_back(inp):
    return(bool(re.match(r"^([Bb]{1}ack[(\(\))]{0,1}[;]{0,1})|(-[Bb]{1}\s*)|(-)$",inp)))

def detect_help(inp):
    return(bool(re.match(r"^(-){,2}[hH]{1}(elp){0,1}\s*$",inp)))

if __name__ == '__main__':
    app.run()

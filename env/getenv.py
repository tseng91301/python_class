
import os
import json

#get environment variable and return the json encoded value
def envjson_d(name):
    return json.loads(os.getenv(name))

#get json encoded value and push into environment variable
def envjson_p(name:str,val:dict):
    os.environ[name]=json.dumps(val)
    return

#get user current mode
def get_mode(uid):
    out=list()
    try:
        mode1=envjson_d(uid+"_mode")
        out.append(mode1["mode"])
        out.extend(mode1["mode_detail"])
    except Exception as e:
        print("At get_mode, "+str(e))
    return out

def set_mode(uid,data:dict):
    mode1={
        "mode":"",
        "mode_detail":[]
    }
    try:
        mode1["mode"]=data[0]
        mode1["mode_detail"]=[]
        for i,val in enumerate(data):
            if(i>0):
                mode1["mode_detail"].append(val)
    except Exception as e:
        print("at set_mode, "+str(e))
    envjson_p(uid+"_mode",mode1)
    return

def get_data(uid):
    return envjson_d(uid+"_data")

def set_data(uid,data):
    envjson_p(uid+"_data",data)
    return

def download_permission(uid,val=-1):
    if(val==-1):
        try:
            return int(os.getenv(uid+"_dl_p"))
        except:
            return 0
    else:
        os.environ[uid+"_dl_p"]=str(val)
        print("download_permission(uid,1)")
        print("dl_p="+os.getenv(uid+"_dl_p"))
        return
    
def upload_permission(uid,val=-1):
    if(val==-1):
        try:
            return int(os.getenv(uid+"_ul_p"))
        except:
            return 0
    else:
        os.environ[uid+"_ul_p"]=str(val)
        return
        

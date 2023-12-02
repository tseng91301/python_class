import re
def detail(mode:list,data,arg):
    ret={}
    try:
        ret["msg"]=""
        if(mode[-1]=="name" and mode[-2]=="basic"):
            data["basic"]["name"]=arg
        if(mode[-1]=="email" and mode[-2]=="basic"):
            data["basic"]["email"]=arg
        if(mode[-1]=="phone" and mode[-2]=="basic"):
            data["basic"]["phone"]=arg
        if(mode[-1]=="address" and mode[-2]=="basic"):
            data["basic"]["address"]=arg
        if((arg in ["name","email","phone","address"]) and mode[-1]=="basic"):
            mode.append(arg)
            ret["msg"]="Please enter your "+arg+"."
        ret["success"]=1
        ret["data"]=data
        ret["mode"]=mode
    except Exception as e:
        ret["success"]=0
        ret["error"]=str(e)
    return ret
    
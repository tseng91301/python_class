import re
def detail(mode,data,arg):
    ret={}
    try:
        if(mode[-1]=="name" and mode[-2]=="basic"):
            data["basic"]["name"]=arg
        if(mode[-1]=="email" and mode[-2]=="basic"):
            data["basic"]["email"]=arg
        if(mode[-1]=="phone" and mode[-2]=="basic"):
            data["basic"]["phone"]=arg
        if(mode[-1]=="address" and mode[-2]=="basic"):
            data["basic"]["address"]=arg
        ret["success"]=1
        ret["data"]=data
    except Exception as e:
        ret["success"]=0
        ret["error"]=str(e)
    return ret
    
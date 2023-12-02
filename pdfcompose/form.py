import re
def detail(mode:list,data,arg:str):
    ret={}
    try:
        goback=0
        inp_f=0
        ret["msg"]=""
        if(mode[-1]=="name" and mode[-2]=="basic"):
            data["basic"]["name"]=arg
            goback=1
            inp_f=1
        elif(mode[-1]=="email" and mode[-2]=="basic"):
            data["basic"]["email"]=arg
            goback=1
            inp_f=1
        elif(mode[-1]=="phone" and mode[-2]=="basic"):
            data["basic"]["phone"]=arg
            goback=1
            inp_f=1
        elif(mode[-1]=="address" and mode[-2]=="basic"):
            data["basic"]["address"]=arg
            goback=1
            inp_f=1
        elif((arg in ["Name","Email","Phone","Address"]) and mode[-1]=="basic"):
            mode.append(arg.lower())
            ret["msg"]="Please enter your "+arg+"."
        else:
            ret["msg"]="Unknown command '"+arg+"' !"
        if(inp_f):
            ret["msg"]="Finish basic -> "+mode[-1]+" input, auto change into basic section."
        if(goback):
            mode.pop()
        ret["success"]=1
        ret["data"]=data
        ret["mode"]=mode
    except Exception as e:
        ret["success"]=0
        ret["error"]=str(e)
    return ret
    
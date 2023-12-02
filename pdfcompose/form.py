import re
def detail(mode:list,data,arg:str):
    ret={}
    try:
        goback=0
        inp_f=0
        ret["msg"]=""
        ret["help"]=0

        # the function used in basic section
        if(check_exist(mode,["basic"])):
            if(check_exist(mode,["name"])):
                data["basic"]["name"]=arg
                goback=1
                inp_f=1
            elif(check_exist(mode,["email"])):
                data["basic"]["email"]=arg
                goback=1
                inp_f=1
            elif(check_exist(mode,["phone"])):
                data["basic"]["phone"]=arg
                goback=1
                inp_f=1
            elif(check_exist(mode,["address"])):
                data["basic"]["address"]=arg
                goback=1
                inp_f=1
            elif(arg in ["Name","Email","Phone","Address"]):
                mode.append(arg.lower())
                ret["msg"]="Please enter your "+arg+"."
            else:
                ret["msg"]="Unknown command in basic '"+arg+"' !"

        # The function used in education section
        elif(check_exist(mode,["education"])):
            if(check_exist(mode,["add"])):
                try:
                    ins_data=arg.split("\n")
                    for n,v in enumerate(ins_data):
                        ins_data[n]=v.strip()
                    data["education"]["info"].append({}) #add one space
                    data["education"]["info"][data["education"]["num"]]["un"]=ins_data[0] #University name, College name
                    data["education"]["info"][data["education"]["num"]]["dn"]=ins_data[1] #Degree name
                    data["education"]["info"][data["education"]["num"]]["ka"]=ins_data[2] #Key achievements
                    data["education"]["info"][data["education"]["num"]]["cc"]=ins_data[3] #University city and country
                    data["education"]["info"][data["education"]["num"]]["gmy"]=ins_data[4] #Graduation month and year
                    data["education"]["num"]+=1
                except:
                    ret["msg"]="Failed to record, please make sure you insert the right way."
                    goback=1
            elif(check_exist(mode,["del"])):
                try:
                    ins_data=int(arg.split(","))
                    print(ins_data)
                    data["education"]["info"]=rmv(data["education"]["info"],ins_data)
                    data["education"]["num"]-=len(ins_data)
                except:
                    ret["msg"]="Failed to delete, please make sure you insert the right way."
                goback=1
            elif arg in ["Add","+"]:
                mode.append("add")
                ret["help"]=1
            elif arg in ["del"]:
                mode.append("del")
                t1="Send a number to delete the following item or use ',' between numbers to delete multiple items.\n\n"
                for n,v in enumerate(data["education"]["info"]):
                    t1+=str(n)+":\n"
                    t1+="   University or College name: "+str(v["un"])+"\n"
                    t1+="   Degree name: "+str(v["dn"])+"\n"
                    t1+="   Key achievements: "+str(v["ka"])+"\n"
                    t1+="   University city and country: "+str(v["cc"])+"\n"
                    t1+="   Graduation month and year: "+str(v["gmy"])+"\n"
                ret["msg"]=t1
        else:
            ret["msg"]="Unknown command in education '"+arg+"' !"
        if(inp_f):
            ret["msg"]="Finish basic -> "+mode[-1]+" input, auto change into basic section."

        # go back by defined times
        for i in range(goback):
            mode.pop()

        # set outcomming message
        ret["success"]=1
        ret["data"]=data
        ret["mode"]=mode
    except Exception as e:
        ret["success"]=0
        ret["error"]=str(e)
    return ret

def check_exist(data:list,inp:list):
    find=0
    try:
        for n1,d1 in enumerate(data):
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
    
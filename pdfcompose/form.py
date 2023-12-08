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
                except:
                    ret["msg"]="Internal server error, thanks for your patience to let us fix it."
                try:
                    data["education"]["info"][data["education"]["num"]]["un"]=ins_data[0] #University name, College name
                    data["education"]["info"][data["education"]["num"]]["dn"]=ins_data[1] #Degree name
                    data["education"]["info"][data["education"]["num"]]["ka"]=ins_data[2] #Key achievements
                    data["education"]["info"][data["education"]["num"]]["cc"]=ins_data[3] #University city and country
                    data["education"]["info"][data["education"]["num"]]["gmy"]=ins_data[4] #Graduation month and year
                    data["education"]["num"]+=1
                    goback=1
                except:
                    ret["msg"]="Failed to record, please make sure you insert the right way and re-send."
                    data["education"]["info"].pop()

            elif(check_exist(mode,["del"])):
                try:
                    ins_data2=arg.split(",")
                    ins_data=list()
                    for v in ins_data2:
                        ins_data.append(int(v))
                    data["education"]["info"]=rmv(data["education"]["info"],ins_data)
                    data["education"]["num"]-=len(ins_data)
                except:
                    ret["msg"]="Failed to delete, please make sure you insert the right way."
                goback=1
            elif arg in ["Add","+"]:
                mode.append("add")
                ret["help"]=1
            elif arg in ["Del"]:
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
                ret["msg"]="Unknown command in basic -> education '"+arg+"' !"
        
        # The function used in professional section
        elif(check_exist(mode,["professional"])):
            if(check_exist(mode,["add"])):
                try:
                    ins_data=arg.split("\n")
                    for n,v in enumerate(ins_data):
                        ins_data[n]=v.strip()
                    data["professional"]["info"].append({}) #add one space
                except:
                    ret["msg"]="Internal server error, thanks for your patience to let us fix it."
                try:
                    data["professional"]["info"][data["professional"]["num"]]["on"]=ins_data[0] #Organization name
                    data["professional"]["info"][data["professional"]["num"]]["p"]=ins_data[1] #Position
                    data["professional"]["info"][data["professional"]["num"]]["ka"]=ins_data[2] #Key achievements
                    data["professional"]["info"][data["professional"]["num"]]["cc"]=ins_data[3] #Work city and country
                    data["professional"]["info"][data["professional"]["num"]]["gmy"]=ins_data[4] # Employment period (Start month, year – End month, year)
                    data["professional"]["num"]+=1
                    goback=1
                except:
                    ret["msg"]="Failed to record, please make sure you insert the right way and re-send."
                    data["professional"]["info"].pop()

            elif(check_exist(mode,["del"])):
                try:
                    ins_data2=arg.split(",")
                    ins_data=list()
                    for v in ins_data2:
                        ins_data.append(int(v))
                    data["professional"]["info"]=rmv(data["professional"]["info"],ins_data)
                    data["professional"]["num"]-=len(ins_data)
                except:
                    ret["msg"]="Failed to delete, please make sure you insert the right way."
                goback=1
            elif arg in ["Add","+"]:
                mode.append("add")
                ret["help"]=1
            elif arg in ["Del"]:
                mode.append("del")
                t1="Send a number to delete the following item or use ',' between numbers to delete multiple items.\n\n"
                for n,v in enumerate(data["professional"]["info"]):
                    t1+=str(n)+":\n"
                    t1+="   Organization name: "+str(v["on"])+"\n"
                    t1+="   Position: "+str(v["p"])+"\n"
                    t1+="   Key achievements: "+str(v["ka"])+"\n"
                    t1+="   city and country: "+str(v["cc"])+"\n"
                    t1+="   Employment period: "+str(v["gmy"])+"\n"
                ret["msg"]=t1
            else:
                ret["msg"]="Unknown command in basic -> professional '"+arg+"' !"

        # The function used in leadership section
        elif(check_exist(mode,["leadership"])):
            if(check_exist(mode,["add"])):
                try:
                    ins_data=arg.split("\n")
                    for n,v in enumerate(ins_data):
                        ins_data[n]=v.strip()
                    data["leadership"]["info"].append({}) #add one space
                except:
                    ret["msg"]="Internal server error, thanks for your patience to let us fix it."
                try:
                    data["leadership"]["info"][data["leadership"]["num"]]["on"]=ins_data[0] #Organization name
                    data["leadership"]["info"][data["leadership"]["num"]]["p"]=ins_data[1] #Position
                    data["leadership"]["info"][data["leadership"]["num"]]["ka"]=ins_data[2] #Key achievements
                    data["leadership"]["info"][data["leadership"]["num"]]["cc"]=ins_data[3] #Work city and country
                    data["leadership"]["info"][data["leadership"]["num"]]["gmy"]=ins_data[4] # Leadership period (Start month, year – End month, year)
                    data["leadership"]["num"]+=1
                    goback=1
                except:
                    ret["msg"]="Failed to record, please make sure you insert the right way and re-send."
                    data["leadership"]["info"].pop()

            elif(check_exist(mode,["del"])):
                try:
                    ins_data2=arg.split(",")
                    ins_data=list()
                    for v in ins_data2:
                        ins_data.append(int(v))
                    data["leadership"]["info"]=rmv(data["leadership"]["info"],ins_data)
                    data["leadership"]["num"]-=len(ins_data)
                except:
                    ret["msg"]="Failed to delete, please make sure you insert the right way."
                goback=1
            elif arg in ["Add","+"]:
                mode.append("add")
                ret["help"]=1
            elif arg in ["Del"]:
                mode.append("del")
                t1="Send a number to delete the following item or use ',' between numbers to delete multiple items.\n\n"
                for n,v in enumerate(data["leadership"]["info"]):
                    t1+=str(n)+":\n"
                    t1+="   Organization name: "+str(v["on"])+"\n"
                    t1+="   Position: "+str(v["p"])+"\n"
                    t1+="   Key achievements: "+str(v["ka"])+"\n"
                    t1+="   city and country: "+str(v["cc"])+"\n"
                    t1+="   Leadership period: "+str(v["gmy"])+"\n"
                ret["msg"]=t1
            else:
                ret["msg"]="Unknown command in basic -> leadership '"+arg+"' !"

        # The function used in certification section
        elif(check_exist(mode,["certification"])):
            if(check_exist(mode,["add"])):
                try:
                    ins_data=arg.split("\n")
                    title=ins_data[0].strip()
                    d1={}
                    d1["t"]=title
                    for n,v in enumerate(ins_data):
                        if(n!=0):
                            l1=ins_data[n].split(":")
                            try:
                                d1[l1[0].strip()]=l1[1].strip()
                            except:
                                continue
                        ins_data[n]=v.strip()
                    data["certification"]["info"].append(d1) #add one space
                    data["certification"]["num"]+=1
                    goback=1
                except:
                    ret["msg"]="Failed to record, please make sure you insert the right way and re-send."
                    data["certification"]["info"].pop()

            elif(check_exist(mode,["del"])):
                try:
                    ins_data2=arg.split(",")
                    ins_data=list()
                    for v in ins_data2:
                        ins_data.append(int(v))
                    data["certification"]["info"]=rmv(data["certification"]["info"],ins_data)
                    data["certification"]["num"]-=len(ins_data)
                except:
                    ret["msg"]="Failed to delete, please make sure you insert the right way."
                goback=1
            elif arg in ["Add","+"]:
                mode.append("add")
                ret["help"]=1
            elif arg in ["Del"]:
                mode.append("del")
                t1="Send a number to delete the following item or use ',' between numbers to delete multiple items.\n\n"
                for n,v in enumerate(data["certification"]["info"]):
                    t1+=str(n)+"("+str(v["t"])+")"+":\n"
                    for n2,v2 in enumerate(v):
                        if(n2==0):
                            continue
                        t1+="   "+v2+": "+v[v2]+"\n"
                ret["msg"]=t1
            else:
                ret["msg"]="Unknown command in basic -> certification '"+arg+"' !"

        # The function used in skill section
        elif(check_exist(mode,["skill"])):
            if(check_exist(mode,["add"])):
                try:
                    ins_data=arg.split("\n")
                    title=ins_data[0].strip()
                    d1={}
                    d1["t"]=title
                    for n,v in enumerate(ins_data):
                        if(n!=0):
                            l1=ins_data[n].split(":")
                            try:
                                d1[l1[0].strip()]=l1[1].strip()
                            except:
                                continue
                        ins_data[n]=v.strip()
                    data["skill"]["info"].append(d1) #add one space
                    data["skill"]["num"]+=1
                    goback=1
                except:
                    ret["msg"]="Failed to record, please make sure you insert the right way and re-send."
                    data["skill"]["info"].pop()

            elif(check_exist(mode,["del"])):
                try:
                    ins_data2=arg.split(",")
                    ins_data=list()
                    for v in ins_data2:
                        ins_data.append(int(v))
                    data["skill"]["info"]=rmv(data["skill"]["info"],ins_data)
                    data["skill"]["num"]-=len(ins_data)
                except:
                    ret["msg"]="Failed to delete, please make sure you insert the right way."
                goback=1
            elif arg in ["Add","+"]:
                mode.append("add")
                ret["help"]=1
                ret["help_back"]=2
            elif arg in ["Del"]:
                mode.append("del")
                t1="Send a number to delete the following item or use ',' between numbers to delete multiple items.\n\n"
                for n,v in enumerate(data["skill"]["info"]):
                    t1+=str(n)+"("+str(v["t"])+")"+":\n"
                    for n2,v2 in enumerate(v):
                        if(n2==0):
                            continue
                        t1+="   "+v2+": "+v[v2]+"\n"
                ret["msg"]=t1
            else:
                ret["msg"]="Unknown command in basic -> skill '"+arg+"' !"
        
        # The function used in additional section
        elif(check_exist(mode,["additional"])):
            if(check_exist(mode,["add"])):
                try:
                    ins_data=arg.split("\n")
                    title=ins_data[0].strip()
                    d1={}
                    d1["t"]=title
                    for n,v in enumerate(ins_data):
                        if(n!=0):
                            l1=ins_data[n].split(":")
                            try:
                                d1[l1[0].strip()]=l1[1].strip()
                            except:
                                continue
                        ins_data[n]=v.strip()
                    data["additional"]["info"].append(d1) #add one space
                    data["additional"]["num"]+=1
                    goback=1
                except:
                    ret["msg"]="Failed to record, please make sure you insert the right way and re-send."
                    data["additional"]["info"].pop()

            elif(check_exist(mode,["del"])):
                try:
                    ins_data2=arg.split(",")
                    ins_data=list()
                    for v in ins_data2:
                        ins_data.append(int(v))
                    data["additional"]["info"]=rmv(data["additional"]["info"],ins_data)
                    data["additional"]["num"]-=len(ins_data)
                except:
                    ret["msg"]="Failed to delete, please make sure you insert the right way."
                goback=1
            elif arg in ["Add","+"]:
                mode.append("add")
                ret["help"]=1
            elif arg in ["Del"]:
                mode.append("del")
                t1="Send a number to delete the following item or use ',' between numbers to delete multiple items.\n\n"
                for n,v in enumerate(data["additional"]["info"]):
                    t1+=str(n)+"("+str(v["t"])+")"+":\n"
                    for n2,v2 in enumerate(v):
                        if(n2==0):
                            continue
                        t1+="   "+v2+": "+v[v2]+"\n"
                ret["msg"]=t1
            else:
                ret["msg"]="Unknown command in basic -> additional '"+arg+"' !"

        # The function when other situation
        else:
            ret["msg"]="Unknown command in basic '"+arg+"' !"
        
        # The function when complete basic insertion
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
    
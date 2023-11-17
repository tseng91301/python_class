def formpdf(cli_id,arg):
    data=json.loads(os.getenv(cli_id+"_data"))
    if(os.getenv(cli_id+"_mode2")=="topic1"):
        data['topic1']=arg
        os.environ[cli_id+"_mode2"] = ""
        os.environ[cli_id+"_data"]=json.dumps(data)
        return "complete topic1 insertion"
    if(os.getenv(cli_id+"_mode2")=="topic2"):
        if(os.getenv(cli_id+"_mode3")=="del"):

        if(arg=="ok"):
            os.environ[cli_id+"_mode2"] = ""
            return "exit topic2 insertion"
        elif(arg=="del"):
            out="Please type the number to del that column :\n"
            out+="to delete multiple data, type ',' between numbers\n"
            for i,v in data['topic2']:
                out+=str(i)+": "+v+"\n"
            return out
        tmp=arg.split('\n')
        data['topic2']=data['topic2']+tmp
        os.environ[cli_id+"_data"]=json.dumps(data)
        return "complete topic2 insertion, if complete insertion, type 'ok'"
    if(os.getenv(cli_id+"_mode2")=="topic3"):
        if(arg=="ok"):
            os.environ[cli_id+"_mode2"] = ""
            return "exit topic3 insertion"
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
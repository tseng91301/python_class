from pdfcompose import form,to_pdf,template
from help.help import help,help_mode

import json
import re

mode=["formpdf"]
data=template.t_data

def formpdf(arg):
    # when not specified step
    global mode
    global data
    if(len(mode)==1):
        # Do something to configuration file
        if(arg=="dump"):
            print(json.dumps(data))
            return
        elif arg in ["Config download","Config-d"]:
            with open("config_data.json",'w') as fo:
                fo.write(json.dumps(data))
                fo.close()
                print("Store the data into config_data.json")
                return
        elif arg in ["Config use","Config upload","Config-u"]:
            try:
                with open("config_data.json",'r') as fi:
                        data=json.loads(fi.read())
                        print("Data read successfully!")
            except Exception as e:
                print("Failed to read data: "+str(e))
            return
            
        # Export pdf file
        elif(re.match(r"^[Ee]{1}xport\s*$",arg)):
            f_string=to_pdf.gen(data).getvalue()
            with open("output.pdf",'wb') as fo:
                fo.write(f_string)
                print("Export successfully!")
                fo.close()
                return
        
        if arg in ["Basic","B","basic"]:
            mode=[mode[0],"basic"]
            print(help_mode(mode))
            return
        if arg in ["Education","Edu"]:
            mode=[mode[0],"education"]
            print(help_mode(mode))
            return
        if arg in ["Professional","Professional experience","Prof"]:
            mode=[mode[0],"professional"]
            print(help_mode(mode))
            return
        if arg in ["Leadership","Lead"]:
            mode=[mode[0],"leadership"]
            print(help_mode(mode))
            return
        if arg in ["Certification","Cert"]:
            mode=[mode[0],"certification"]
            print(help_mode(mode))
            return
        if arg in ["Skill","Skills"]:
            mode=[mode[0],"skill"]
            print(help_mode(mode))
            return
        if arg in ["Additional","Plus"]:
            mode=[mode[0],"additional"]
            print(help_mode(mode))
            return
        
        print("Unknown command '"+arg+"' !")
        return
    
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
    print(ret)
    return

def detect_exit(inp):
    return(bool(re.match(r"^[Ee]{1}xit[(\(\))]{0,1}[;]{0,1}[\n]*",inp)))

def detect_back(inp):
    return(bool(re.match(r"^([Bb]{1}ack[(\(\))]{0,1}[;]{0,1})|(-[Bb]{1}\s*)|(-)$",inp)))

def detect_help(inp):
    return(bool(re.match(r"^(-){,2}[hH]{1}(elp){0,1}\s*$",inp)))

def handle_message(msg):
    global mode
    if detect_back(msg):
        if(len(mode)==1):
            print("You are on the top of the program")
            return
        else:
            mode.pop()
            print(f"You are at {mode[0]} -> {mode[-1]}")
    elif detect_exit(msg):
        print("Bye Bye ~")
        return -1
    elif detect_help(msg):
        print(help_mode(mode))
    else:formpdf(msg)

while(1):
    msgin=input(f"\n{json.dumps(mode)}Input the command >>> ")
    t1=handle_message(msgin)
    try:
        if(t1==-1):
            break
    except:
        continue
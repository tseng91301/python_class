import os
absp=os.path.dirname(os.path.abspath(__file__))
def help(arg="main"):
    if(arg=="-"):
        arg="main"
    try:
        rep=open(os.path.join(absp,arg+".txt")).read()
        return rep
    except Exception as e:
        return "Failed to show help message "+arg+" :\n"+str(e)

def help_mode(mode):
    helpinfo=""
    try:
        helpinfo=str(mode[0])+"-"
        helpinfo=helpinfo+str(mode[-1])
    except Exception as e:
        print(str(e))
    t1=help(helpinfo)
    return t1
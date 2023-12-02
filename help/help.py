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

def help_mode(mode,startl=1,endl=1):
    helpinfo=""
    try:
        for n,v in enumerate(mode):
            if(n<startl):
                if(n!=0):
                    helpinfo+="-"
                helpinfo+=str(v)
        helpinfo+="-"
        for n,v in enumerate(reversed(mode)):
            if(n<endl):
                if(n!=0):
                    helpinfo+="-"
                helpinfo+=str(v)
    except Exception as e:
        print(str(e))
    t1=help(helpinfo)
    return t1
def tomd(datain):
    out=""
    out+="# "+datain['topic1']+"\n"
    out+="---\n"
    for i,v in enumerate(datain['topic2']):
        out+=str(i+1)+". "+str(v)+"\n"
    for i,v in enumerate(datain['topic3']):
        out+="### "+str(v)+": "+datain['topic3'][v]+"\n"
    return out
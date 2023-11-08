import re

input_string = open("sendcmupload/testre.txt",'r').read()

# 定义正则表达式模式

#pattern=r'textarea'
#pattern=r'(?<=height:5px\"\>)https://send.cm/d/[^/](?=\</textarea\>)'
pattern=r'(?<=height:5px">).*?(?=<\/textarea>)'
#<textarea class="form-control" style="overflow:hidden ; height:5px">https://send.cm/d/lHgf</textarea>
dl_link=re.search(pattern,input_string)
print(dl_link.group(0))
import requests
from io import BytesIO
import re
import json
from datetime import datetime

sendcm_first_url="https://send.cm/upload"
sendcm_first_response=requests.get(sendcm_first_url)
if(sendcm_first_response.status_code==200):
    t1=sendcm_first_response.text
    pattern = r'https://[^/]+.send.cm/cgi-bin/upload.cgi\?[^\s]+(?=\")'
    upload_location=re.search(pattern,t1).group(0)
    #print(upload_location)
else:
    print("Get upload location failed with status code [{sendcm_first_response.status_code}]")

# 定义虚拟文件内容
file_content = "Hello, this is a virtual file content.fsdfsfsfds"
file_content = file_content.encode('utf-8')


# 创建一个 BytesIO 对象，用于模拟文件对象
virtual_file = BytesIO(file_content)

upl_form_data={
    "utype":"anon",
    "file_expire_unit":"DAY",
    "keepalive":1
}

response=requests.post(upload_location,data=upl_form_data,files={str(datetime.now())+'.txt':virtual_file})
#response=requests.post(upload_location,data=upl_form_data)
print(response.status_code)
print(response.text)

file_id=json.loads(response.text)[0]['file_code']
if(file_id=="undef"):
    print("Failed to upload file, remote banned")

sendcm_getlink_url="https://send.cm/?op=upload_result&st=OK&fn="+file_id
t1=requests.get(sendcm_getlink_url).text
dl_link=(re.search(r'(?<=height:5px">).*?(?=<\/textarea>)',t1)).group(0)
print(dl_link)

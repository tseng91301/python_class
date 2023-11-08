import requests
import re
import json

sendcm_first_url="https://send.cm/upload"
sendcm_first_response=requests.get(sendcm_first_url)
if(sendcm_first_response.status_code==200):
    t1=sendcm_first_response.text
    pattern = r'https://[^/]+.send.cm/cgi-bin/upload.cgi\?[^\s]+(?=\")'
    upload_location=re.search(pattern,t1).group(0)
    #print(upload_location)
else:
    print("Get upload location failed with status code [{sendcm_first_response.status_code}]")

upl_form_data={
    "utype":"anon",
    "file_expire_unit":"DAY",
    "keepalive":1
}

response=requests.post(upload_location,data=upl_form_data,files={'file_0':open("test.pdf",'rb')})
print(response.status_code)
print(response.text)

file_id=json.loads(response.text)[0]['file_code']
if(file_id=="undef"):
    print("Failed to upload file, remote banned")
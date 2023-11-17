import re
input_text="a1:a2\nb1: b2"
tmp=input_text.split('\n')
tmp2={}
for con in tmp:
    tmp3=re.split(r":(\s)*",con,1)
    print(tmp3)
    tmp2[tmp3[0]]=tmp3[2]

print(str(tmp2))
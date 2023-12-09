from flask import Flask, make_response, request
import json

app = Flask(__name__)

dd={
    "Name":"xx",
    "values":[
        "1213",
        234324,
        "ggg"
    ]
}

@app.route('/download', methods=['GET'])
def download():
    if request.method=='GET':
        op=int(request.values['op'])
        uid=request.values['uid']
        if(1==op):
            if(op==1): #Operation to download file
                response=make_response(str(json.dumps(dd)))
                response.headers['Content-Disposition'] = 'attachment; filename='+uid+'.json'
                return response

if __name__ == '__main__':
    app.run(debug=True)

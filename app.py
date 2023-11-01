from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/helloname', methods=['GET'])
def helloname():
    if request.method == 'GET': 
        return 'Hello ' + request.values['username'] 
@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()

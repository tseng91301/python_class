from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    if request.method == 'GET':
        op=int(request.values['op'])
        uid = request.values.get('uid')

        if op == 1:
            # 执行文件下载的操作

            # 创建响应对象
            response = make_response('文件下载内容')

            # 设置Content-Disposition头，指定下载的文件名
            response.headers['Content-Disposition'] = 'attachment; filename='+uid+'.txt'

            return response

if __name__ == '__main__':
    app.run(debug=True)

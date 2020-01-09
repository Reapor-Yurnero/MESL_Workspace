import os
import random
import jwt
import requests
from flask import Flask, render_template, send_from_directory, jsonify, request, Response


app = Flask(__name__)
node_modules = os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_modules")


@app.route('/node_modules/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(node_modules, path)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/api/<path:path>')
def api(path):
    auth = request.headers.get('Authorization')
    if auth.startswith('bearer '):
        token = auth[7:]
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        uid = payload["userid"]
        appname = payload["appname"]
        if appname == 'power':
            newurl = 'http://127.0.0.1:5001/'
            print(newurl)
        elif appname == 'temperature':
            newurl = 'http://127.0.0.1:5002/'
            print(newurl)
        elif appname == 'headcount':
            newurl = 'http://127.0.0.1:5003/'
            print(newurl)
        else:
            print("unknown app/user identification")
            newurl = request.host_url

        resp = requests.request(
            method=request.method,
            url=request.url.replace(request.host_url, newurl),
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        response = Response(resp.content, resp.status_code, headers)
        print(response)
        return response
    else:
        print('not a valid bearer authorization entry')
        return jsonify({'message': 'failed'})
    # if path == 'get_average_power':
    #     newurl = '127.0.0.1:5001'


    #
    # return jsonify({
    #     'message': 'success',
    #     'value': random.random()
    # })

    # newurl += '/api/'+path




if __name__ == '__main__':
    app.run()

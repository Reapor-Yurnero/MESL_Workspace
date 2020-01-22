import os
import jwt
import requests
from flask import Flask, render_template, send_from_directory, jsonify, request, Response
import app_management
import redis
import iptables_manager

redis_host = "localhost"
redis_port = 6379
redis_password = ""
redis_db = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)


app = Flask(__name__)
node_modules = os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_modules")


@app.route('/node_modules/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(node_modules, path)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/app/app1')
def render_app1():
    print("run /app/app1")
    cname = app_management.spawn_app("app1", "fxh")  # user name is hard coded here, can be fetched with multiple methods
    iptables_manager.grant_host_access(cname, redis_db.get(cname),"tcp","5001")
    return render_template('app1.html')


@app.route('/app/app2')
def render_app2():
    print("run /app/app2")
    cname = app_management.spawn_app("app2", "fxh")  # user name is hard coded here, can be fetched with multiple methods
    # iptables_manager.grant_host_access(cname, redis_db.get(cname),"tcp","5000")
    return render_template('app2.html')


@app.route('/app/app3')
def render_app3():
    print("run /app/app3")
    cname = app_management.spawn_app("app3", "fxh")  # user name is hard coded here, can be fetched with multiple methods
    iptables_manager.grant_external_access(cname, redis_db.get(cname),"tcp","47.254.124.205","2222")
    return render_template('app3.html')


@app.route('/api/<path:path>')
def api(path):
    auth = request.headers.get('Authorization')
    if auth.startswith('bearer '):
        token = auth[7:]
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload["userid"]
        appname = payload["appname"]
        # if appname == 'app1':
        #     newurl = 'http://127.0.0.1:5001/'
        #     print(newurl)
        # elif appname == 'temperature':
        #     newurl = 'http://127.0.0.1:5002/'
        #     print(newurl)
        # elif appname == 'headcount':
        #     newurl = 'http://127.0.0.1:5003/'
        #     print(newurl)
        if path == "exit":
            print("stopping "+appname + "-" + user_id)
            app_management.stop_container(appname + "-" + user_id)
            return jsonify({
                'message': 'success'
            })
        container_ip = redis_db.get(appname + "-" + user_id)
        if container_ip is not None:
            newurl = 'http://'+container_ip+':5000/'  # TODO: should allow customized port in the future
        else:
            print("unknown app/user identification")
            newurl = request.host_url
        print(newurl)
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
    app.run(host="0.0.0.0")

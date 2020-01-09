# MESL Workspace

## APP Management

A function library for app management including register app, spawn app, run/stop/rm app and control internet accessibility of app

A text documentation for the APIs generated by docstring can be find [here](./app_management/docs/build/text/app_management.txt) or download the html [here](./app_management/docs/build/html/app_management.html) and open with a browser.

### System Setup

Before we start, the system environment should be prepared. 

```sudo sh init.sh```

What the script does first is to generate an isolated bridge docker network `isolated_nw` with linux interface name `docker1` (the default one is `docker0`). The purpose is to separate the image building network environment (in `docker0`) from the application image working network (`docker1`).

The script then manipulate the iptables rules such that
* No communication with the external world by default
* No communication with the host by default except the tcp/udp connection with high ephemeral ports (ephemeral ports would be used when a tcp channel is established by system e.g. browser visiting a website and we want to allow this happening as host might need to query docker services. Security is not compromised as long as host don't put any useful service on ephemeral ports)

This will enforce the isolation of applications (dockers).


### Usage

A few usage examples are listed in `example.py`. Here's a procedure on testing the functionality.

#### Example 1

Open a python3 console
```python
import app_management
app_management.register_app("hello_world_web", "latest", "./hello_world_web", "python index.py", "python:3", 5000, "pip install -r requirements.txt")
cname = app_management.spawn_app("hello_world_web", "user001")
print(app_management.get_container_ip(cname))
```
A simple hello world flask web app is built and spawned. You will get its ip address, let's say it's 172.25.0.2

Open the browser and visit 172.25.0.2:5000 or `curl 172.25.0.2:5000` and you will see "Hello World". 

This example shows that visit from host to dockers on ephemeral ports are not blocked.

#### Example 2

To run this example, the default parameter of app_spawn need to change '-d' to '-it' as the test application here is interactive and will be terminated immediately if ran detached (receiving EOF). 

Open a terminal
```
python3 ./server/server.py
```
A server application will be ran locally on 2222 port.

Open a python3 console
```python
import app_management
app_management.register_app("clientapp", "latest", "./docker_client", "python client.py", "python:3", 5000)
app_management.spawn_app("clientapp", "user001", "172.25.0.1 2222")
```
A client application targeting at the server program will be ran inside a docker container. Follow the prompt and try to get the flight information then you will find it get stuck. This is because this client is trying to communicate with the server app through udp at port 2222 on host, which is blocked by default

Run another python3 console and grant the host connection
```python
import app_management
app_management.grant_host_access("clientapp:user001", "udp", "2222")

```
You find the stuck request will proceed successfully. 

This example shows how we block and allow the connection between docker app and host.

#### Example 3

Similar to example 2, this time the server is ran on a remote server. Refer to `example.py`.

This example shows how we block and allow the connection between docker app and host.

### Limitation

In dev, I didn't consider docker build/run error as they are really rare. (Build would still succeed even if the app itself is not working.) To handle this, some py-docker lib might be needed. But I think they are heavy and unreliable to some extents as well.

The iptables rules are difficult to be deleted once added. But I recently realize that it's necessary to have this function. There are two potential solutions: based on string operation after getting the whole table, we counted the order of rules and find the position of the target rule and delete it as usual; use a py-iptables lib, which is heavy and difficult to be used as well


## Request Router

The request router is demo program which shows how a flask app can forward the request it received to designated target server.


Install the libs

```
pip3 install -r requirements.txt
npm install
```

Run the router and all three dummy apps.
```
python3 app.py
python3 dummy_apps/app1/index.py
python3 dummy_apps/app2/index.py
python3 dummy_apps/app3/index.py
```

Open `127.0.0.1:5000` and you will see three buttons. These three buttons will get response from three dummy apps' backends respectively, while all requests are sent to the router directly. Three different jwg token (user_id + appname) is hardcoded for these three buttons' requests, and used by the router to determine where's the correct destination.
 
The router should be incorporated into the brick frontend, and those destination server should be the corresponding application backend per user. We probably need a database to save this mapping between app+user and address.

A universal api rule might be needed for route filtering. e.g. all applications' api should be like /api/xxx
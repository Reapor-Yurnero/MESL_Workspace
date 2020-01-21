import app_management

# test suit 1
app_management.register_app("hello_world_web", "latest", "./hello_world_web", "python index.py", "python:3", 5000
                            , "pip install -r requirements.txt")
cname = app_management.spawn_app("hello_world_web", "user001")
print(app_management.get_container_ip(cname))

# test suit 2
app_management.register_app("clientapp", "latest", "./docker_client", "python client.py", "python:3", 5000)
app_management.spawn_app("clientapp", "user001", "172.25.0.1 2222")
# app_management.grant_host_access("clientapp:user001", "udp", "2222")

# test sult 3
app_management.register_app("clientapp", "latest", "./docker_client", "python client.py", "python:3", 5000)
cname = app_management.spawn_app("clientapp", "user002", "47.254.124.205 2222")
# app_management.grant_external_access("clientapp:user002", "udp", ["47.254.124.205", "2222"])
import app_management
import iptables_manager

if __name__ == '__main__':
    # test suit 1
    # app_management.register_app("hello_world_web", "latest", "app_management/hello_world_web", "python index.py", "python:3", 5000
    #                             , "pip install -r requirements.txt")
    # cname = app_management.spawn_app("hello_world_web", "user001")
    # print(app_management.get_container_ip("hello_world_web-user001"))

    # test suit 2
    # res = app_management.register_app("clientapp", "latest", "./docker_client", "python client.py", "python:3", 5000)
    # app_management.spawn_app("clientapp", "user001", "172.25.0.1 2222")
    # # app_management.grant_host_access("clientapp:user001", "udp", "2222")
    # iptables_manager.grant_host_access("clientapp:user001", "udp", "2222")

    # test sult 3
    app_management.register_app("clientapp", "latest", "./app_management/docker_client", "python client.py", "python:3", 5000)
    cname = app_management.spawn_app("clientapp", "remote", "47.254.124.205 2222")
    print(cname)
    # print(app_management.get_container_ip("clientapp-remote"))
    # iptables_manager.grant_external_access("clientapp-remote", "172.25.0.2", "udp", "47.254.124.205", "2222")

import app_management


if __name__ == "__main__":
    app_management.register_app("app1","latest","dummy_apps/app1","python index.py", "python:3", 5000, "pip install -r requirements.txt")
    app_management.register_app("app2", "latest", "dummy_apps/app2", "python index.py", "python:3", 5000, "pip install -r requirements.txt")
    app_management.register_app("app3", "latest", "dummy_apps/app3", "python index.py", "python:3", 5000, "pip install -r requirements.txt")
    # print(app_management.spawn_app("app2", "fxh"))
    # print(app_management.get_container_id("app2-fxh"))


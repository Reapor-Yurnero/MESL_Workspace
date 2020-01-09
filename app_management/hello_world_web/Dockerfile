FROM python:3
COPY . /hello_world_web
WORKDIR /hello_world_web
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "index.py"]
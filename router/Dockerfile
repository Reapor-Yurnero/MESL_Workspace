FROM nikolaik/python-nodejs
COPY . /toy_web
WORKDIR /toy_web
RUN pip install -r requirements.txt && npm install 
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]
from flask import Flask, jsonify
import random
app = Flask(__name__)


@app.route("/api/get_temperature")
def get_temp():
    return jsonify({
        'message': 'success',
        'value': random.randrange(-40,40)
    })


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)

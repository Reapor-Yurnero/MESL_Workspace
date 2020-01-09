from flask import Flask, jsonify
import random
app = Flask(__name__)


@app.route("/api/get_average_power")
def hello():
    return jsonify({
        'message': 'success',
        'value': random.randrange(100,150)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5001"), debug=True)

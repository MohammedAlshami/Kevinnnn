from flask import Flask
from flask import render_template
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route('/dummy_response', methods=['POST',"GET"])
def dummy_response():
    data = request.get_json()
    message = data.get('message')

    # Modified dummy response JSON
    response = {
        "body": {
            "message": "This is a dummy response from the bot."
        }
    }

    return jsonify(response)

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route('/dummy_response', methods=['POST', 'GET'])
def dummy_response():
    if request.method == 'POST':
        data = request.get_json()  # This extracts JSON data from the request body
        if data is None:
            # If no JSON found in the request, respond with an error
            return jsonify({"error": "No JSON payload provided"}), 400

        # Extract message if it exists
        message = data.get('message', 'No message provided')
    else:
        # If the request is GET, we could define a default action or error
        message = 'GET request received, no message provided'

    # Prepare a dummy response JSON
    response = {
        "body": {
            "message": f"This is a dummy response from the bot. {message}"
            }
    }

    return jsonify(response)
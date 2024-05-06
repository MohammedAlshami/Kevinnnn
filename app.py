from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
from openai import OpenAI

client = OpenAI(api_key="sk-proj-Xv3f361sX1D16LGAF0HmT3BlbkFJFgsAHypJVxLBawuPb2XK")


def chat_response(query):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ]
    )
    return completion.choices[0].message


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
        message = chat_response(message)
    else:
        # If the request is GET, we could define a default action or error
        message = 'GET request received, no message provided'

    # Prepare a dummy response JSON
    response = {
        "body": {
            "message": f"{message}"
            }
    }

    return jsonify(response)
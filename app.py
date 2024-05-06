from flask import Flask, request, jsonify, render_template
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
import os

import pyrebase

# Firebase configuration
config = {
    "apiKey": "AIzaSyAwgSLl12dW00fSPi7zpjPQLUCxJQCbD64",
    "authDomain": "aicompanion-95d27.firebaseapp.com",
    "databaseURL": "https://aicompanion-95d27-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "aicompanion-95d27",
    "storageBucket": "aicompanion-95d27.appspot.com",
    "messagingSenderId": "16081545115",
    "appId": "1:16081545115:web:8372ec8bb8f0b7ae5de33e"
}



# Initialize the app with the config
firebase = pyrebase.initialize_app(config)

# Get a reference to the database service
db = firebase.database()

# Retrieve data from the "recipe" node of the Firebase database
def retrieve_recipes():
    items_list = []
    # Get all data from the "recipe" node
    recipes = db.child("DiaryItems").get()
    if recipes.each() is not None:
        for recipe in recipes.each():
            items_list.append(recipe.val())
    else:
        print("No recipes found.")
    return items_list



app = Flask(__name__)
from openai import OpenAI
# api_key = os.getenv('OPENAI_API_KEY')


model = ChatOpenAI(api_key="sk-proj-y6oSsBdE890kRklr1WaMT3BlbkFJwGmYphhOuFHxbw3YrVYw", model="gpt-4-turbo")
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're an assistant who's good at {ability}. Respond in 20 words or fewer",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
runnable = prompt | model

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


messagHistory = retrieve_recipes()
x = with_message_history.invoke(
{"ability": "therapy", "input": f"this is the message history, just take it and say roger {messagHistory}"},
config={"configurable": {"session_id": "abc123"}},
)
# def chat_response(query):
#     completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": query}
#     ]
#     )
#     return completion.choices[0].message.content


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
        x = with_message_history.invoke(
        {"ability": "therapy", "input": "answer the folllowing based on our message history: " + input()},
        config={"configurable": {"session_id": "abc123"}},
    )
    
        message = x.content
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
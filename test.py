from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI

query = "hello"
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

x = with_message_history.invoke(
    {"ability": "therapy", "input": "What does love mean?"},
    config={"configurable": {"session_id": "abc123"}},
)


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

messagHistory = retrieve_recipes()
x = with_message_history.invoke(
{"ability": "therapy", "input": f"this is the message history, just take it and say roger {messagHistory}"},
config={"configurable": {"session_id": "abc123"}},
)

while True:
    x = with_message_history.invoke(
    {"ability": "therapy", "input": "" + input()},
    config={"configurable": {"session_id": "abc123"}},
)
    print(x.content)
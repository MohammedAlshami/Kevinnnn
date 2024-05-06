import pyrebase

# Firebase configuration
config = {
 "apiKey": "AIzaSyBLv1DiRB6egmpaoIKfjODXZF5fYheQKIM",
  "authDomain": "realtimedatabasetest-f226a.firebaseapp.com",
  "databaseURL":
    "https://realtimedatabasetest-f226a-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "realtimedatabasetest-f226a",
  "storageBucket": "realtimedatabasetest-f226a.appspot.com",
  "messagingSenderId": "348704796176",
  "appId": "1:348704796176:web:38994c5ab4d54b752ce495",
}

# Initialize the app with the config
firebase = pyrebase.initialize_app(config)

# Get a reference to the database service
db = firebase.database()

# Retrieve data from the "recipe" node of the Firebase database
def retrieve_recipes():
    items_list = []
    # Get all data from the "recipe" node
    recipes = db.child("Posts").get()
    if recipes.each() is not None:
        for recipe in recipes.each():
            items_list.append(recipe.val())
    else:
        print("No recipes found.")
    return items_list

if __name__ == "__main__":
    print(retrieve_recipes())

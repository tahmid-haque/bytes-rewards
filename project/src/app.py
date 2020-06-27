"""
This is the main component of our project. It is be used to connect the whole
app together and provide a way to start a server.
"""

from flask import Flask, render_template, request, redirect, url_for
from database import *

app = Flask(__name__)  # Initialize a flask app using current file
db = Database.get_instance(app)  # Get a database instance

valueIndex = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", \
"q", "r", "s", "t", "u", "v", "w", "x", "y"]

@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        #I used default user b/c we dont have accounts yet
        goals, user = db.query('goals'), db.queryGoal('restaurant_users', {"username": "Victor Chang"})  # Retrieve list of all goals in goals database
        return render_template('index.j2', goals = goals, user_goals = user)   # Render the home page using the goals variable
    except QueryFailureException:
        return "There was an issue locating your goals."

@app.route('/remove-goal', methods=['POST'])
def remove():
    value = request.form.get('g')
    try:
        goals, user = db.query('goals'), db.deleteGoal('restaurant_users', {"username": "Victor Chang"}, value)  # Retrieve list of all goals in goals database
        render_template('index.j2', user_goals = user) # Render the home page using the goals variable
        return redirect('/')
    except QueryFailureException:
        return "There was an issue locating your goals."

@app.route('/add-goal', methods=['POST'])
def add():
    values = [request.form.get(x) for x in valueIndex]
    try:
        goals = db.query('goals'),   # Retrieve list of all goals in goals database
        for i in range(len(values)):
            if values[i] == None:
                continue
            else:
                user = db.addGoal('restaurant_users', {"username": "Victor Chang"}, values[i], i) # Add goal in relative position
                render_template('index.j2', user_goals = user) # Render the home page using the goals variable
        return redirect('/')
    except QueryFailureException:
        return "There was an issue locating your goals."

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
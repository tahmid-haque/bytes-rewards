"""
This is the main component of our project. It is be used to connect the whole
app together and provide a way to start a server.
"""

from flask import Flask, render_template, request, redirect, url_for
from database import *

app = Flask(__name__)  # Initialize a flask app using current file
db = Database.get_instance(app)  # Get a database instance

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
    id = request.form.get('g')
    try:
        goals, user = db.query('goals'), db.deleteGoal('restaurant_users', {"username": "Victor Chang"}, id)  # Retrieve list of all goals in goals database
        render_template('index.j2', user_goals = user)
        return redirect('/')
    except QueryFailureException:
        return "There was an issue locating your goals."


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
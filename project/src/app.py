"""
This is the main component of our project. It is be used to connect the whole
app together and provide a way to start a server.
"""

from flask import Flask, render_template, request, redirect, url_for
from restaurantProfileManagement import restaurantProfileManager

app = Flask(__name__)  # Initialize a flask app using current file

@app.route('/')
def index():
    rpm = restaurantProfileManager(app, "Victor Chang")
    goals = rpm.get_goals()
    bingo_board = rpm.get_bingo_board()
    return render_template('index.j2',  # Render the home page using the goals variable
        goals = goals, 
        board_name = bingo_board["name"],
        board = bingo_board["board"]
    ) 

@app.route('/save', methods=['POST'])
def save():
    rpm = restaurantProfileManager(app, "Victor Chang")
    name = request.form["board_name"]
    board = request.form.getlist("board[]")
    rpm.set_bingo_board(name, board)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
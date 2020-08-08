"""
This file contains routes related to verifying customer goals
"""

from flask import Blueprint, request, redirect, flash, jsonify
from flask_login import current_user, login_required

bp = Blueprint("verification", __name__)


@bp.route('/verify-goal/<string:code_data>', methods=['POST', 'GET'])
@login_required
def verify_goal(code_data):
    """
    This route is used in the ajax call to return a json object for when a qr code is scanned.
    """
    data = code_data.split("+")
    goals = current_user.get_goals()
    goal = ""
    for goal in goals:
        if str(goal['_id']) == data[1]:
            return jsonify({'goal': goal['goal']})

    return jsonify({'goal': "No Goal Found"})


@bp.route('/finish-goal', methods=['POST', 'GET'])
@login_required
def finish_goal():
    """
    This route retrieves a code, and adds a goal as completed to the database.
    Redirects to the qr goal verification page when done.
    """
    data = request.form["code"].split("+")
    if len(data) != 3:
        flash("Invalid QR code!")
        return redirect("/profile/qr-verification")
    user = data[0]
    goal_id = data[1]
    position = data[2]
    msg = current_user.complete_goal(user, goal_id, position)
    flash(msg)
    return redirect("/profile/qr-verification")

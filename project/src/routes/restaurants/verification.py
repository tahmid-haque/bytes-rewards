"""
This file contains routes related to verifying customer goals and rewards
"""

from flask import Blueprint, request, redirect, flash, jsonify
from flask_login import current_user, login_required

bp = Blueprint("verification", __name__)


@bp.route('/verify', methods=['POST'])
@login_required
def verify():
    """
    This route is used in the ajax call to return a json object for when a qr code is scanned.
    """
    data = request.form["data"].split("+")

    if len(data) == 3:
        goals = current_user.get_goals()
        for goal in goals:
            if str(goal['_id']) == data[1]:
                return jsonify({'goal': goal['goal']})

    elif len(data) == 4:
        rewards = current_user.get_rewards()
        for reward in rewards:
            if str(reward['_id']) == data[1]:
                return jsonify({'reward': reward['reward']})

    return jsonify({'message': "Invalid QR Code!"})


@bp.route('/finish-goal', methods=['POST'])
@login_required
def finish_goal():
    """
    This route retrieves a code, and adds a goal as completed to the database.
    Redirects to the qr goal verification page when done.
    """
    data = request.form["code"].split("+")
    if len(data) != 3:
        return jsonify({'message': "Invalid QR code!"})
    user = data[0]
    goal_id = data[1]
    position = data[2]
    msg = current_user.complete_goal(user, goal_id, position)
    return jsonify({'message': msg})


@bp.route('/finish-reward', methods=['POST'])
@login_required
def finish_reward():
    """
    This route retrieves a code, and adds a reward as completed to the database.
    Redirects to the qr reward verification page when done.
    """
    code = request.form["code"]
    data = code.split("+")
    if len(data) != 4:
        return jsonify({'message': "Invalid QR code!"})
    user = data[0]
    reward_id = data[1]
    position = data[2]
    msg = current_user.complete_reward(user, code)
    return jsonify({'message': msg})


"""
This file contains routes related to a restaurant user's game board.
"""

from flask import Blueprint, render_template, request, redirect
from flask_login import current_user, login_required

bp = Blueprint("board", __name__)


@bp.route('/')
@login_required
def view_board():
    """
    When retrieving this route, get a restaurant profile's goals and bingo
    board. Render these items together to show a bingo editor.
    """
    goals = current_user.get_goals(
    )  # current_user is loaded from load_user so get goals
    bingo_board = current_user.get_bingo_board()
    rewards = current_user.get_rewards()
    return render_template('view_game_board.j2',
                           goals=goals,
                           board_name=bingo_board["name"],
                           rewards=rewards,
                           board=bingo_board["board"],
                           board_reward=bingo_board["board_reward"])


@bp.route('/save', methods=['POST'])
@login_required
def save():
    """
    When posting to this route, save a bingo board to the restaurant profile
    using the request body. Redirect to the bingo editor on completion.
    """
    name = request.form["board_name"]
    board = request.form.getlist("board[]")
    board_reward = request.form.getlist("board_reward[]")
    current_user.set_bingo_board(name, board, board_reward)
    return redirect("/")

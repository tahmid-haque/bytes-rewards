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
    When retrieving this route, get a restaurant profile's current bingo
    board. Render these items together to show current bingo board and expiration date.
    """
    rest_id = current_user.get_restaurant_id()
    try:
        bingo_board = current_user.get_restaurant_board_by_id(rest_id)
        return render_template(
        'view_game_board.j2',
        goals=[x['goal'] for x in bingo_board["board"]],
        board_name=bingo_board["name"],
        rewards=[x['reward'] for x in bingo_board["board_reward"]],
        board_size=bingo_board["size"],
        current_expiry=str(bingo_board["expiry_date"]))
    except KeyError:
        return redirect("/board/edit")


@bp.route('/edit')
@login_required
def edit_board():
    """
    When retrieving this route, get a restaurant profile's goals, rewards and future
    board. Render these items together to show a bingo editor.
    """
    goals = current_user.get_goals(
    )  # current_user is loaded from load_user so get goals
    bingo_board = current_user.get_future_board()
    rewards = current_user.get_rewards()
    current_expiry = current_user.get_current_board_expiry()
    return render_template('edit_game_board.j2',
                           goals=goals,
                           board_name=bingo_board["name"],
                           rewards=rewards,
                           board=bingo_board["board"],
                           board_reward=bingo_board["board_reward"],
                           board_size=bingo_board["size"],
                           current_expiry=current_expiry,
                           future_expiry=bingo_board["expiry_date"])


@bp.route('/save', methods=['POST'])
@login_required
def save():
    """
    When posting to this route, save a bingo board to the restaurant profile
    using the request body. Redirect to the bingo editor on completion.
    """
    bingo_board = {
        "name": request.form["board_name"],
        "size": int(request.form["size"]),
        "expiry_date": request.form["expiry_date"],
        "board": request.form.getlist("board[]"),
        "board_reward": request.form.getlist("board_reward[]"),
    }
    current_user.set_bingo_board(bingo_board)
    return redirect("/board/edit")

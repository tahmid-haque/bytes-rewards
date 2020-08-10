"""
This file contains routes related to restaurant profiles.
"""

from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required
from modules.restaurant_profile_manager import RestaurantProfileManager

bp = Blueprint("profile", __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def view_profiles():
    """
    Allows users to view restaurant profiles that are set to public.
    """
    restaurant_profiles = RestaurantProfileManager("").get_public_profiles()
    favourite = current_user.get_favourite()
    return render_template('view_profiles.j2',
                           profiles=restaurant_profiles,
                           favourite=favourite)


@bp.route('/<string:obj_id>/board', methods=['GET', 'POST'])
@login_required
def view_board(obj_id):
    """
    Allows users to view the chosen restaurant's game board.
    """
    username = current_user.get_id()
    rpm = RestaurantProfileManager("")
    rpm.update_board(obj_id)
    board = rpm.get_restaurant_board_by_id(obj_id)
    current_user.set_board_progress(board, obj_id)
    board["expiry_date"] = board["expiry_date"].strftime(
        "%B X%d, %Y - X%I:%M %p UTC").replace("X0", "X").replace("X", "")
    return render_template('view_game_board.j2',
                           goals=board["board"],
                           name=board["name"],
                           rewards=board["board_reward"],
                           cust_id=username,
                           size=board["size"],
                           date=board["expiry_date"])


@bp.route('/<string:obj_id>/reset-board', methods=['GET', 'POST'])
@login_required
def reset_board(obj_id):
    """
    When posting to this route, reset the bingo board goals.
    Redirect to the bingo board on completion.
    """
    current_user.reset_complete_board(obj_id)
    return redirect("board")


@bp.route('/<string:prof_id>/profile', methods=['GET', 'POST'])
@login_required
def view_restaurant_profile(prof_id):
    """
    Allows users to view the chosen restaurant's profile.
    """
    rpm = RestaurantProfileManager("")
    rest_info = rpm.get_restaurant_profile_by_id(prof_id)
    return render_template('view_profile.j2',
                           restaurant_name=rest_info["name"],
                           address=rest_info["location"]["address"],
                           city=rest_info["location"]["city"],
                           province=rest_info["location"]["province"],
                           postal_code=rest_info["location"]["postal_code"],
                           phone_number=rest_info["phone_number"],
                           category=rest_info["category"],
                           rest_img=rest_info["image"],
                           description=rest_info["description"])


@bp.route('/<string:obj_id>/favourite', methods=['GET', 'POST'])
@login_required
def favourite_restaurant(obj_id):
    """
    Allows users to add and remove restaurants from "favourite"
    """
    current_user.update_favourite(obj_id)
    return redirect("/")


@bp.route('/view-favourites', methods=['GET', 'POST'])
@login_required
def view_favourites():
    """
    Allows users to view restaurants from "favourite"
    """
    favourite = current_user.get_favourite()
    rpm = RestaurantProfileManager("")
    profiles = rpm.get_public_profiles()
    list_fav = current_user.get_favourite_doc(profiles, favourite)
    return render_template('view_favourites.j2',
                           profiles=list_fav,
                           favourite=favourite)


@bp.route('/view-favourites/<string:obj_id>/favourite', methods=['GET', 'POST'])
@login_required
def view_favourite_restaurant(obj_id):
    """
    Allows users to remove restaurants from "favourite" while on "favourites" page
    """
    current_user.update_favourite(obj_id)
    return redirect('/profiles/view-favourites')

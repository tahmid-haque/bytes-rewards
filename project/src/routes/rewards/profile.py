"""
This file contains routes related to restaurant profiles.
"""

from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required
from modules.restaurant_profile_manager import RestaurantProfileManager
from modules.customer_profile_manager import CustomerProfileManager

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
    board = rpm.get_restaurant_board_by_id(obj_id)
    current_user.set_board_progress(board, obj_id)
    return render_template('view_game_board.j2',
                           goals=board["board"],
                           name=board["name"],
                           rewards=board["board_reward"],
                           cust_id=username,
                           size=board["size"],
                           date=board["expiry_date"])


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

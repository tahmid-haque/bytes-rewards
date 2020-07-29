"""
This file contains routes related to a restaurant user's profile.
"""

from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required

bp = Blueprint("profile", __name__)


@bp.route('/')
@login_required
def view_profile():
    """
    Displays the current user's restaurant profile page.
    """
    rest_info = current_user.get_profile()
    if rest_info == {}:
        flash("Please create a restaurant profile to continue.")
        return redirect("/profile/edit")
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


@bp.route('/edit')
@login_required
def edit_profile():
    """
    Display the edit restaurant profile page.
    Prerequisite: User is logged in.
    """
    profile = current_user.get_profile()
    ready_for_publish = current_user.get_bingo_board()["board"] != []
    return render_template('edit_profile.j2', profile=profile, allow_public=ready_for_publish)


@bp.route('/save', methods=['POST'])
@login_required
def save_profile():
    """
    Save a restaurant profile using the provided data.
    Prerequisite: User is logged in.
    """
    profile = {key: val for key, val in request.form.items() if '[' not in key}
    profile["location"] = {}
    for key in request.form:  # Add location items to profile
        if '[' in key:
            profile["location"][key[9:-1]] = request.form[key]
    current_user.update_profile(profile)
    return redirect("/")

@bp.route('/qr-verification')
@login_required
def view_qr_verification():
    """
    Display the qr verification page.
    Prerequisite: User is logged in.
    """
    return render_template('qr-verification.html')
"""
This file houses the unit test suite for the restaurant view restaurant profile page"
"""

import os
import sys
import pytest
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder

from restaurants_app import app
from modules.owner.restaurant_profile_manager import RestaurantProfileManager
from modules.owner.public_profile import PublicProfileModifier


@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def test_view_profile_route_logged_in(client):
    """
    Test that restauarant view restaurant profile page loads when the user is logged in.
    """
    client.post("/login", data={"username": "janedoe", "password": "Aa123456"})
    res = client.get("/profile", follow_redirects=True)
    assert b"Profile" in res.data


def test_get_profile():
    """
    Test that a user is able to retrieve their profile when they are logged in.
    """
    rpm = RestaurantProfileManager("janedoe")
    pm = PublicProfileModifier(rpm)
    profile = pm.get_profile()
    expected_profile = {
        "name":
            "Cinco de Mayo",
        "category":
            "Mexican",
        "image":
            "https://images.squarespace-cdn.com/content/v1/5841c30e2e69cf1ae4538068/148182"
            +
            "6250798-5WPYGJ0K1Y6XAKP068MO/ke17ZwdGBToddI8pDm48kB6N0s8PWtX2k_eW8krg04V7gQa3"
            +
            "H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5C"
            +
            "VlOqpeNLcJ80NK65_fV7S1URWK2DJDpV27WG7FD5VZsfFVodF6E_6KI51EW1dNf095hdyjf10zfCEV"
            + "Hp52s13p8g/Matteson-0005.jpg?format=1000w",
        "description":
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
            +
            "incididunt ut labore et dolore magna aliqua. At erat pellentesque adipiscing "
            +
            "commodo elit at imperdiet. Aenean pharetra magna ac placerat vestibulum lectus"
            +
            " mauris ultrices eros. Commodo viverra maecenas accumsan lacus vel facilisis"
            +
            " volutpat. Nibh sed pulvinar proin gravida hendrerit. Egestas erat imperdiet"
            +
            " sed euismod nisi porta lorem. Id eu nisl nunc mi. Sodales neque sodales ut"
            +
            " etiam sit amet nisl purus. Quam lacus suspendisse faucibus interdum posuere"
            +
            " lorem ipsum dolor. Quis imperdiet massa tincidunt nunc pulvinar sapien et. "
            +
            "Vitae congue eu consequat ac felis donec. Tristique et egestas quis ipsum "
            +
            "suspendisse ultrices gravida. Accumsan lacus vel facilisis volutpat est."
            +
            " Convallis convallis tellus id interdum velit laoreet id donec. Pellentesque "
            +
            "dignissim enim sit amet. Est sit amet facilisis magna. Mauris cursus "
            +
            "mattis molestie a iaculis at erat. Sem viverra aliquet eget sit. Semper risus in"
            +
            " hendrerit gravida rutrum quisque non tellus orci. Et malesuada fames "
            + "ac turpis egestas.",
        "phone_number":
            "(555)555-5555",
        "is_public":
            True,
        "location": {
            "address": "123 Road St.",
            "postal_code": "A1C 2B3",
            "city": "Toronto",
            "province": "ON"
        }
    }

    assert profile == expected_profile

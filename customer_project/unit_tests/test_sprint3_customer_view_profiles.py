"""
This file houses the unit test suite for the customer view restaurant profile page"
"""


import os
import sys
import pytest
from bson.objectid import ObjectId
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../src'))   # Import the src folder


from app import app
from customer_profile_manager import CustomerProfileManager


@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def test_edit_profile_route_logged_in(client):
    """
    Test that customer view restaurant profile page loads when the user is logged in.
    """
    client.post("/customer_login",
                data={
                    "username": "unitTestUser",
                    "password": "Password!"
                })
    res = client.get("/view_profiles", follow_redirects=True)
    assert b"Choose a Game Board" in res.data


def test_get_restaurant_profiles():
    """
    Test that get_restaurant_profiles() function in customer_profile_manager.py retreives all
    restaurant profile fields that are public.
    """
    rpm = CustomerProfileManager(app, "unitTestUser")
    profiles = rpm.get_restaurant_profiles()
    expected_profiles = {\
    ObjectId("5f01f3046225761eae99dcae"):
    {
        "name":
            "Restaurant Name",
        "category":
            "Chinese",
        "image":
            "https://media-cdn.tripadvisor.com/media/photo-s/15/5b/d8/1c/sea-food-and-champagne.jpg",
        "description":
            "Good restaurant",
        "phone_number":
            "1111111111",
        "is_public":
            True,
        "location":
            {
                "address":
                    "123 Street",
                "postal_code":
                    "A1B2C3",
                "city":
                    "Richmond Hill",
                "province":
                    "ON"
            }
        },
        ObjectId("5f0506544ccce5aae5c0a859"):
        {
            "name":
                "Jake's",
            "category":
                "BBQ",
            "image":
                "https://restaurantengine.com/wp-content/uploads/2015/05/startup-restaurants-typically-overspend.jpg",
            "description":
                "It's a pretty good bbq place.",
            "phone_number":
                "4166543785",
            "is_public":
                True,
            "location":
                {
                    "address":
                        "1265 Military Trail",
                    "postal_code":
                        "M1C1A4",
                    "city":
                        "Toronto",
                    "province":
                        "ON"
                }
        },
        ObjectId("5f0610136eba8be14fd07522"):
        {
            "name":
                "Too Good To Be True",
            "category":
                "",
            "image":
                "https://www.thescottishsun.co.uk/wp-content/uploads/sites/2/2017/04/gord21.jpg",
            "description":
                "Best restaurant you will ever visit",
            "phone_number":
                "4167208989",
            "is_public":
                True,
            "location":
                {
                    "address":
                        "The moon",
                    "postal_code":
                        "M1J1J3",
                    "city":
                        "Scarborough",
                    "province":
                        "ON"
                }
        },
        ObjectId("5f0a1295f73575fbc66fcd90"):
        {
            "name":
                "Cinco de Mayo",
            "category":
                "Mexican",
            "image":
                "https://images.squarespace-cdn.com/content/v1/5841c30e2e69cf1ae4538068/1481826250798-5WPYGJ0K1Y6XAKP068MO/ke17ZwdGBToddI8pDm48kB6N0s8PWtX2k_eW8krg04V7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z5QPOohDIaIeljMHgDF5CVlOqpeNLcJ80NK65_fV7S1URWK2DJDpV27WG7FD5VZsfFVodF6E_6KI51EW1dNf095hdyjf10zfCEVHp52s13p8g/Matteson-0005.jpg?format=1000w",
            "location":
                {
                    "province":
                        "ON",
                    "city":
                        "Toronto",
                    "postal_code":
                        "A1C 2B3",
                    "address":
                        "123 Road St."
                },
            "description":
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. At erat pellentesque adipiscing commodo elit at imperdiet. Aenean pharetra magna ac placerat vestibulum lectus mauris ultrices eros. Commodo viverra maecenas accumsan lacus vel facilisis volutpat. Nibh sed pulvinar proin gravida hendrerit. Egestas erat imperdiet sed euismod nisi porta lorem. Id eu nisl nunc mi. Sodales neque sodales ut etiam sit amet nisl purus. Quam lacus suspendisse faucibus interdum posuere lorem ipsum dolor. Quis imperdiet massa tincidunt nunc pulvinar sapien et. Vitae congue eu consequat ac felis donec. Tristique et egestas quis ipsum suspendisse ultrices gravida. Accumsan lacus vel facilisis volutpat est. Convallis convallis tellus id interdum velit laoreet id donec. Pellentesque dignissim enim sit amet. Est sit amet facilisis magna. Mauris cursus mattis molestie a iaculis at erat. Sem viverra aliquet eget sit. Semper risus in hendrerit gravida rutrum quisque non tellus orci. Et malesuada fames ac turpis egestas.",
            "phone_number":
                "(555)555-5555",
            "is_public":
                True
        },
        ObjectId("5f0a71210005421728659412"):
        {
            "name":
                "Popeyes",
            "category":
                "Chicken",
            "image":
                "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Popeyes_Logo_With_Symbol_2019.svg/1200px-Popeyes_Logo_With_Symbol_2019.svg.png",
            "description":
                "Decent fried chicken.",
            "phone_number":
                "4162358904",
            "location":
                {
                    "address":
                        "2500 Danforth Ave",
                    "postal_code":
                        "M4C1L2",
                    "city":
                        "Toronto",
                    "province":
                        "ON"
                },
            "is_public":
                True
        }
    }
    assert profiles == expected_profiles

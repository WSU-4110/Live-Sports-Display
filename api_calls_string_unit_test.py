from api_calls_string import *
import pytest
import os



# ----------------Unit test 1-------------------------------------------------
# Tests for percentages (Trust me, this function was there from the start).
#   And it better count - it's one of EXACTLY six functions that make sense to
#   test. 

# testing with set values value
def percent_test(made, attempted, expected):
    actual = per(made, attempted)

    assert expected == actual


# Main testing function
def percent_test_parts():
    # testing with middle values
    percent_test(27,55,49.0)

    # testing with minimum values
    percent_test(0,24,0.0)

    # testing with near minimum values
    percent_test(1,19,5.2)


    # testing with near maximum values
    percent_test(37,39,94.8)

    # testing with maximum values
    percent_test(7,7,100.0)

    # testing with 0 div 0
    percent_test(0,0,0.0)



# ----------------Unit test 2-------------------------------------------------
# Tests for # ----------------Unit test 1-------------------------------------------------
# Tests for get_season_player_stats_from_id(player_id)


#If the API website is having issues, the tests are irrelevant.
# And yes, it is reliably successful - as long as the API website doesn't
# have issues
def test_season_stats():
    
    # invalid id
    player_id = "NotAnId"
    expected = None
    actual = get_season_player_stats_from_id(player_id)
    assert expected == actual



    player_id = "8ec91366-faea-4196-bbfd-b8fab7434795"
    expected_begins = "Name: Drew Eubanks"
    actual = get_season_player_stats_from_id(player_id)

    assert expected_begins == actual[0:len(expected_begins)]
    


    
#percent_test_parts()
#test_season_stats()

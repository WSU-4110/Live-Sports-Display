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

# ----------------Unit test 3-------------------------------------------------
# Tests for team_playingQ(hour_start, hour_end, dayOf)

# Will not be valid after April: the games on the 12th will change,
# and the only way to write a unit test to check that would be to
# rewrite the function
def test_teams_playingQ():

    # no games
    hour_start = 0
    hour_end = 18
    dayOf = 12
    expected = []
    actual = team_playingQ(hour_start, hour_end, dayOf)
    assert expected == actual

    # first games
    hour_start = 0
    hour_end = 19
    dayOf = 3
    expected = []
    expected.append(["583ec97e-fb46-11e1-82cb-f4ce4684ea4c","583ed056-fb46-11e1-82cb-f4ce4684ea4c","7bac8648-0372-436f-a8b3-90567f732aae"])
    expected.append(["583ec8d4-fb46-11e1-82cb-f4ce4684ea4c","583ecae2-fb46-11e1-82cb-f4ce4684ea4c","c4ab090e-9a7d-416a-b949-f7f5b5d8f339"])
    expected.append(["583ecb8f-fb46-11e1-82cb-f4ce4684ea4c","583ec928-fb46-11e1-82cb-f4ce4684ea4c","16aed93b-cb1f-46a0-b68e-513f4d61faaa"])
    expected.append(["583eccfa-fb46-11e1-82cb-f4ce4684ea4c","583ecfff-fb46-11e1-82cb-f4ce4684ea4c","1e59b606-e2e3-46ed-b9ed-be115bd160c5"])
    expected.append(["583ec9d6-fb46-11e1-82cb-f4ce4684ea4c","583ec7cd-fb46-11e1-82cb-f4ce4684ea4c","d07098c0-a722-4ebe-9787-fc06bf26acb5"])

    actual = team_playingQ(hour_start, hour_end, dayOf)
    assert expected == actual

    # all games
    hour_start = 0
    hour_end = 24
    dayOf = 4
    expected = []
    expected.append(["583ecf50-fb46-11e1-82cb-f4ce4684ea4c","583ecb8f-fb46-11e1-82cb-f4ce4684ea4c","2a12cef9-1615-4ec6-a709-bdf4cfb1aae7"])
    expected.append(["583ecea6-fb46-11e1-82cb-f4ce4684ea4c","583ec87d-fb46-11e1-82cb-f4ce4684ea4c","34a90621-b50e-4cbc-93dd-74a7c4216eb0"])
    expected.append(["583ec70e-fb46-11e1-82cb-f4ce4684ea4c","583ed0ac-fb46-11e1-82cb-f4ce4684ea4c","34d50d9b-e65d-42bb-aecc-8efc7a90ba5a"])
    expected.append(["583ecb3a-fb46-11e1-82cb-f4ce4684ea4c","583ec825-fb46-11e1-82cb-f4ce4684ea4c","ba926890-b722-4628-aac6-1963963d8e83"])
    expected.append(["583ecdfb-fb46-11e1-82cb-f4ce4684ea4c","583ed102-fb46-11e1-82cb-f4ce4684ea4c","2d62d8ab-f6fd-45b2-94f7-49622180067f"])
    actual = team_playingQ(hour_start, hour_end, dayOf)
    assert expected == actual

    # last games
    hour_start = 22
    hour_end = 23
    dayOf = 10
    expected = []
    expected.append(["583ed102-fb46-11e1-82cb-f4ce4684ea4c","583eca2f-fb46-11e1-82cb-f4ce4684ea4c","a891c88e-97de-4629-8f6f-2445e8f0fe52"])
    expected.append(["583ecdfb-fb46-11e1-82cb-f4ce4684ea4c","583ecfa8-fb46-11e1-82cb-f4ce4684ea4c","f9998a42-9c4e-41b4-bd98-0c30012b331c"])
    actual = team_playingQ(hour_start, hour_end, dayOf)
    assert expected == actual

    # middle game
    hour_start = 21
    hour_end = 21
    dayOf = 9
    expected = []
    expected.append(["583ece50-fb46-11e1-82cb-f4ce4684ea4c","583ed102-fb46-11e1-82cb-f4ce4684ea4c","b880678a-cacc-49c5-bb1e-e592e86b1e89"])
    actual = team_playingQ(hour_start, hour_end, dayOf)
    assert expected == actual
    


    
#percent_test_parts()
#test_season_stats()

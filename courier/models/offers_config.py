# This module holds the information about
# the List 0f available OFFERS and their validity details

# IDEAL way is to set this up to a Database.
# But considering the scale of this application,
# only a Conf file is used

OFFERS = {
    "OFR001": {
        "discount": 10,
        "distance_range": {
            "min": 0,
            "max": 200,
        },
        "weight_range": {
            "min": 70,
            "max": 200,
        },
    },
    "OFR002": {
        "discount": 7,
        "distance_range": {
            "min": 50,
            "max": 150,
        },
        "weight_range": {
            "min": 100,
            "max": 250,
        },
    },
    "OFR003": {
        "discount": 5,
        "distance_range": {
            "min": 50,
            "max": 250,
        },
        "weight_range": {
            "min": 10,
            "max": 150,
        },
    },
}

# -*- coding: utf-8 -*-

from collections import OrderedDict

COUNTRIES_LIST = [
    ("STJ", "Saint John"),
    ("MTL", "Montreal"),
    ("OTT", "Ottawa"),
    ("TOR", "Toronto"),
    ("CAL", "Calgary"),
    ("VAN", "Vancouver"),
]

# Nicely titled (and translatable) country names.
COUNTRIES_DICT = OrderedDict(COUNTRIES_LIST)

# List of countries suitable for use in forms
# TODO: CTFd 4.0 Move SELECT_COUNTRIES_LIST into constants
SELECT_COUNTRIES_LIST = [("", "")] + COUNTRIES_LIST


def get_countries():
    return COUNTRIES_DICT


def lookup_country_code(country_code):
    return COUNTRIES_DICT.get(country_code)

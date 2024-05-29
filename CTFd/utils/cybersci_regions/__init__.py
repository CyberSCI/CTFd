# -*- coding: utf-8 -*-
from collections import OrderedDict

REGIONS_LIST = [
    ("CAL", "Calgary"),
    ("MTL", "Montreal"),
    ("OTT", "Ottawa"),
    ("STJ", "Saint John"),
    ("TOR", "Toronto"),
    ("VAN", "Vancouver"),
    ("", "Visitor"),
]

# Nicely titled (and translatable) country names.
REGIONS_DICT = OrderedDict(REGIONS_LIST)

# List of countries suitable for use in forms
# TODO: CTFd 4.0 Move SELECT_REGIONS_LIST into constants
SELECT_REGIONS_LIST = REGIONS_LIST


def get_regions():
    return REGIONS_DICT


def lookup_region_code(region_code):
    return REGIONS_DICT.get(region_code)

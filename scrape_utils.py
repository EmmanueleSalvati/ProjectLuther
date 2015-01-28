"""This module contains utility functions to scrape web data"""


# DATAFRAME MANIPULATION UTILITIES
def money_to_int(moneystring):
    """Input: a string like '$33,449,086';
    Output: 33449086"""

    return moneystring.replace(',', '').replace('$', '')


def remove_comma(number):
    """Input: 1,100; Output: 1100"""

    return int(number.replace(",", ''))

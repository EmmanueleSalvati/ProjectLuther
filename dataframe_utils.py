"""Module with utility functions for pandas DataFrames"""
import numpy as np


def str_to_datetime(datestr):
    """Takes a string like 7/31/92 and returns a datetime object"""

    from dateutil import parser
    from datetime import datetime

    date = parser.parse(datestr)
    return date


def find_non_numeric(pd_series):
    """Turns a dash string into a zero"""

    numeric = []
    for elem in pd_series:
        if not elem.isdigit():
            numeric.append(np.nan)
        else:
            numeric.append(int(elem))

    return numeric


def polish_dataframe(df):
    """Minor things: turns strings to int and gets rid of dashes"""

    df['TotalGross'] = df['TotalGross'].apply(int)
    df['OpenGross'] = df['OpenGross'].apply(int)
    df['Rank'] = df['Rank'].apply(int)
    df['TotalTheaters'] = find_non_numeric(df['TotalTheaters'])

    return df


def dt64_to_dt(dt64_list):
    """Returns a list of datetime objects from a list of numpy.datetime64"""

    from datetime import datetime
    ns = 1e-9
    dt_list = []
    for dt64 in dt64_list:
        dt_list.append(datetime.utcfromtimestamp(dt64.astype(int) * ns))

    return dt_list

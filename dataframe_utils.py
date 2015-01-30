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


def get_unmerged_titles(df_boxoffice, df_imdb):
    """Give data frames of BoxOfficeMojo and IMDB, return list of unmatched
    titles"""

    unmatched = df_boxoffice.loc[df_boxoffice.index.
                                 isin(df_imdb.index) is False]

    return unmatched.index


# IF WE WANT TO MERGE BoxOfficeMojo and IMDB DATAFRAMES
def reindex_imdb_titles(df, boxoffice_series):
    """Take df index (imdb movie titles) and gets rid of punctuation,
    capitalization, etc. Returns a dataframe with a new index"""

    bad_index = df.index
    print 'Starting the reindexing...\n'
    print boxoffice_series
    for title in bad_index:
        if title in boxoffice_series:
            print 'found one!', title


def list_of_genres_no_political(pd_series):
    """Loop over the column of genres and return a list of all genres"""

    genres = []
    for genre_list in pd_series:
        for genre in genre_list:
            if genre not in genres:
                genres.append(genre)

    return genres


def genre_counts_no_political(genre_column, genre_list):
    """Input: the series of genres in the dataframe and the list of genres;
    output: a dictionary genre: counts"""

    genres_dict = {}

    for genre in genre_list:
        genres_dict[genre] = 0

    for movie_genres in genre_column:
        for genre in movie_genres:
            genres_dict[genre] += 1

    return genres_dict


def genre_counts(df):
    """Returns a dictionary (genre): counts which includes the Political
    column"""

    # genre_list = list_of_genres_no_political(df['imdbGenres'])

    genre_list = ['Documentary', 'Musical', 'Biography', 'Comedy', 'Music',
                  'History', 'War', 'Crime', 'Mystery', 'Drama', 'Sport',
                  'Family', 'Action', 'Adventure', 'Romance', 'Animation',
                  'Western', 'News', 'Horror', 'Fantasy', 'Thriller',
                  'Sci-Fi', 'Romance', 'Animation', 'Western', 'News',
                  'Horror', 'Fantasy', 'Thriller', 'Sci-Fi', 'Romance',
                  'Animation', 'Western', 'News', 'Horror', 'Fantasy',
                  'Thriller', 'Sci-Fi']

    genre_dict = genre_counts_no_political(df['imdbGenres'], genre_list)
    genre_dict['Political'] = int(df['Political'].sum())

    return genre_dict


def add_genre_columns(df):
    """Take the movies dataframe and add the relevant genre columns"""

    df['Music'] = 0.
    df['War'] = 0.
    df['Drama'] = 0.
    df['History'] = 0.
    df['Sport'] = 0.
    df['Biography'] = 0.

    df_copy = df.copy()
    for title in df.index:
        genre_list = df.loc[title, 'imdbGenres']
        if 'Music' in genre_list:
            df_copy.loc[title, 'Music'] = 1
        if 'War' in genre_list:
            df_copy.loc[title, 'War'] = 1
        if 'Drama' in genre_list:
            df_copy.loc[title, 'Drama'] = 1
        if 'History' in genre_list:
            df_copy.loc[title, 'History'] = 1
        if 'Sport' in genre_list:
            df_copy.loc[title, 'Sport'] = 1
        if 'Biography' in genre_list:
            df_copy.loc[title, 'Biography'] = 1

    return df_copy


def split_by_date(df):
    """Splits the dataframe into before and after Farenheit 9/11"""

    split_date = df.ix['Fahrenheit 9/11'].RelDate
    early = df[df.RelDate < split_date]
    late = df[df.RelDate > split_date]

    return early, late


def uncategorized(df):
    """Return the number of documentaries which
    were not categorized on IMDB"""

    counter = 0
    for movie in df.index:
        if len(df.loc[movie, 'imdbGenres']) == 1 and\
           df.loc[movie, 'Political'] == 0:
            counter += 1

    return counter


def add_uncategorized_column(df):
    """Add one extra feature to the dataframe: Uncategorized"""

    df_copy = df.copy()
    df_copy['Uncategorized'] = 0
    for movie in df.index:
        if len(df.loc[movie, 'imdbGenres']) == 1 and\
           df.loc[movie, 'Political'] == 0:
            df_copy.loc[movie, 'Uncategorized'] = 1

    return df_copy


# LINEAR-REGRESSION-RELATED FUNCTIONS
def train_test_samples(df):
    """Splits a dataframe into 75% train and 25% test"""

    from math import floor

    shuffled_df = df.reindex(np.random.permutation(df.index))

    seventy_five_percent = int(floor(len(shuffled_df) * 0.75))
    train_df = shuffled_df.iloc[:seventy_five_percent, ]
    test_df = shuffled_df.iloc[seventy_five_percent:, ]

    return train_df, test_df




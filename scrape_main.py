"""This is the main file to run to scrape movies"""

import sys
sys.path.append('/Users/JerkFace/Metis/Projects/Luther/')

import scrape_utils
import BoxOffice_utils
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import numpy as np
import pickle as pkl


def list_links(url, pklname):
    """Input: a url string; a pickle file name string;
    Output: a selenium driver with that link"""

    if not url:
        url = sys.argv[1]
    firefox = BoxOffice_utils.driver_with_url(url)
    links_dict = BoxOffice_utils.urls_dict(firefox)
    with open(pklname, 'w') as pklfile:
        pkl.dump(links_dict, pklfile)

    return links_dict


if __name__ == '__main__':

    url = 'http://boxofficemojo.com/genres/chart/?id=politicaldoc.htm'

    ARGS = sys.argv[1:]
    if len(ARGS) > 0:
        url = ARGS[0]

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)

    # Scrape the table and put it into a dictionary
    nav_tabs = soup.find(class_='nav_tabs')
    movie_table = BoxOffice_utils.find_following_table(nav_tabs)
    movie_dict = BoxOffice_utils.table_to_dict(movie_table)

    # Put dictionary into a Dataframe
    movies = pd.DataFrame.from_dict(movie_dict, orient='index')
    movies.columns = ['Rank', 'Studio', 'TotalGross', 'TotalTheaters',
                      'OpenGross', 'OpenTheatres', 'RelDate']
    movies.replace('n/a', np.nan, inplace=True)
    movies = movies.dropna()
    movies['RelDate'] = movies['RelDate'].astype(datetime)
    movies['TotalGross'] = movies['TotalGross'].\
        apply(scrape_utils.money_to_int)
    movies['OpenGross'] = movies['OpenGross'].apply(scrape_utils.money_to_int)
    movies['TotalTheaters'] = movies['TotalTheaters'].\
        apply(scrape_utils.remove_comma)
    movies['OpenTheatres'] = movies['OpenTheatres'].\
        apply(scrape_utils.remove_comma)
    print movies.head()

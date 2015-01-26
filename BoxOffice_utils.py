"""Module that contains utility functions to scrape BoxOfficeMojo data"""
from selenium import webdriver
import pickle as pkl
from bs4 import BeautifulSoup
import urllib2
import pandas as pd
from datetime import datetime
import scrape_utils
import numpy as np


# SCRAPING UTILITIES
def find_following_table(soup_tag):
    """Given an object of type <class 'bs4.element.Tag'>,
    find the first table after it"""

    next_tag = soup_tag.findNextSibling('table')
    if next_tag:
        return next_tag
    else:
        next_tag = find_following_table(next_tag)

    return next_tag


def table_to_dict(soup_table_tag):
    """Input: a table of type <class 'bs4.element.Tag'>,
    Output: a dict {title: [features]}"""

    movie_dict = {}
    for row in soup_table_tag.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) == 8:
            rank = str(cells[0].find(text=True))
            title = str(cells[1].find(text=True))
            studio = str(cells[2].find(text=True))
            tot_gross = str(cells[3].find(text=True))
            tot_theatres = str(cells[4].find(text=True))
            opn_gross = str(cells[5].find(text=True))
            opn_theatres = str(cells[6].find(text=True))
            rel_date = str(cells[7].find(text=True))
            print title
            movie_dict[title] = [rank, studio, tot_gross, tot_theatres,
                                 opn_gross, opn_theatres, rel_date]
    return movie_dict


def driver_with_url(politics_url):
    """Input: http://boxofficemojo.com/genres/chart/?id=politicaldoc.htm
    Output: urls of lists of political documentary"""

    firefox = webdriver.Firefox()
    firefox.get(politics_url)

    return firefox


def urls_dict(firefox):
    """Input: a driver with url;
    Output: a dictionary (page_range): (corresponding url)"""

    print 'Creating dict...'
    links_dict = {}
    page_selector = ('//a[contains(@href, '
                     '"/genres/chart/?view=main&sort=gross")]')
    links_dict['first'] = str(firefox.current_url)

    for page_anchor in firefox.find_elements_by_xpath(page_selector):
        movies_range = str(page_anchor.text)
        href = str(page_anchor.get_attribute('href'))
        links_dict[movies_range] = href

    return links_dict


def page_soup(url):
    """It returns a soup from the url"""

    print url
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)

    return soup


def get_all_movies(pklfilename):
    """Input: a pkl file with the dict of all urls;
    output: a big fat dict with all the movies in it"""

    big_fat_dict = {}

    with open(pklfilename) as pklfile:
        all_dicts = pkl.load(pklfile)
        for url_link in all_dicts.itervalues():
            soup = page_soup(url_link)
            nav_tabs = soup.find(class_='nav_tabs')
            movie_table = find_following_table(nav_tabs)
            movie_dict = table_to_dict(movie_table)
            big_fat_dict.update(movie_dict)

    return big_fat_dict


def dict_to_dataframe(movie_dict):
    """Input: the big fat movie dictionary;
    Output: pandas dataframe"""

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
        apply(scrape_utils.money_to_int)

    movies['OpenTheatres'] = movies['OpenTheatres'].\
        apply(scrape_utils.remove_comma)

    return movies

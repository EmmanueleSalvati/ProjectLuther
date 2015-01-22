"""This module contains utility functions to scrape web data"""

import urllib2
from bs4 import BeautifulSoup
import re


def table_from_soup(soup_obj):
    """Given a BeautifulSoup object in BoxOfficeMojo, returns the movies'
    table... WRONG!!"""

    nav_tabs = soup_obj.find(class_="nav_tabs")
    movie_table = (nav_tabs.findNextSibling().findNextSibling().
                   findNextSibling().findNextSibling())

    return movie_table


def movie_links_from_table(movie_table):
    """Creates and returns a dictionary (movie title): (movie link);

    It takes a soup table as input, it retrieves all the links and
    finally creates the dictionary"""

    movies = {}
    links_from_table = movie_table.find_all('a')
    for links in links_from_table:
        link = links.get('href')
        movie = re.match('/movies/', link)
        if movie:
            movies[links.text] = 'boxofficemojo.com' + link

    return movies


def find_following_table(soup_tag):
    """Given an object of type <class 'bs4.element.Tag'>,
    find the first table after it"""

    next_tag = soup_tag.findNextSibling('table')
    if next_tag:
        return next_tag
    else:
        next_tag = find_following_table(next_tag)

    return next_tag


class movie(object):
    """This class contains the following attributes:
    title, lifetime gross, lifetime theaters, release date, perhaps more"""

    def __init__(self, title=None, life_gross=None, life_theaters=None,
                 rank=None, studio=None, opening_gross=None,
                 opening_theaters=None, rel_date=None):
        self.title = title
        self.life_gross = life_gross
        self.life_theaters = life_theaters
        self.rank = rank
        self.studio = studio
        self.opening_gross = opening_gross
        self.opening_theaters = opening_theaters
        self.rel_date = rel_date




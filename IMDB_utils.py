"""Module that contains utility functions to scrape IMDB data"""

from selenium import webdriver
import re
import urllib2
from bs4 import BeautifulSoup
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('latin-1')


def click_next(firefox):
    """Find the Next button and click it"""
    # firefox = webdriver.Firefox()
    # firefox.get("http://www.imdb.com/search/"
    #             "title?at=0&sort=moviemeter&title_type=documentary")

    buttons = firefox.find_elements_by_class_name('pagination')
    if len(buttons) == 0:
        print "No Next button found!"

    for button in buttons:
        next_button = button.find_element_by_tag_name('a')
        next_string_u = next_button.text
        if re.match('Next', next_string_u):
            print 'Changing page...'
            next_button.click()
            break
        else:
            continue


def movies_list(url):
    """Input: current url; output the list of movies"""

    url = firefox.current_url
    page = urllib2.urlopen(url)
    soap = BeautifulSoup(page)
    movies = soap.findAll(class_='even detailed')
    movies.extend(soap.findAll(class_='odd detailed'))
    # print len(movies)

    return movies


def get_title(cell_soap):
    """Input: a cell soap from IMDB; output: movie title"""

    title = cell_soap.find('a')
    return str(title.text)


def get_link(cell_soap):
    """Input: a cell soap from IMDB; output: movie IMDB link"""

    link = cell_soap.find('a')
    return 'www.imdb.com/' + link.get('href')


def get_year(cell_soap):
    """Input: a cell soap from IMDB; output: movie year"""

    year_class = cell_soap.find('span', {'class': 'year_type'})
    year_text = str(year_class.text)
    year_list = year_text.split()[0]
    year = year_list.replace('(', '')

    return year


def get_user_rating(cell_soap):
    """Input: a cell soap from IMDB; output: movie user rating"""

    # ratings = cell_soap.div.find_all('span', {'class': 'rating-rating'})
    # rating = cell_soap.div.div.get('title')
    # full_string = rating.split()
    # return full_string[3]

    rating = cell_soap.find('span', {'class': 'rating-rating'})
    return str(rating.span.text)


def get_num_voters(cell_soap):
    """Input: a cell soap from IMDB; output: movie number of voters"""

    rating = cell_soap.div.div.get('title')
    full_string = rating.split()

    return full_string[4].replace('(', '').replace(',', '')


def name_and_link(list_of_names):
    """Input: [<a href="/name/nm0688636/">Laura Poitras</a>]
    Output: ('Laura Poitras', "/name/nm0688636/")"""

    names = []
    links = []
    for elem in list_of_names:
        names.append(elem.text)
        links.append(elem.get('href'))

    return (names, links)


def remove_commas_from_list(list_of_names):
    """Remove commas from a list and returns the list"""

    index_list = []
    for i in range(len(list_of_names)):
        if i % 2 != 0:
            index_list.append(i)

    index_list.reverse()
    for index in index_list:
        list_of_names.pop(index)

    return list_of_names


def get_directors_and_actors_list(cell_soap):
    """Input: a cell soap movie from IMDB;
    output: movie list of directors and actors"""

    directors = []
    actors = []

    children_list = []  # tmp list
    movie_credits = cell_soap.find('span', attrs={'class': 'credit'})
    for credit in movie_credits.children:
        children_list.append(credit)

    dir_num = 0
    with_num = 0
    for credit in children_list:
        if 'Dir' in credit:
            dir_num = children_list.index(credit)
        if 'With' in credit:
            with_num = children_list.index(credit)

    directors.extend(children_list[dir_num + 1: with_num])
    actors.extend(children_list[with_num + 1:])

    return (directors, actors)


def directors_names(dirs_list):
    """Takes a list of <a href objects> and strips out a list of names of
    directors"""

    remove_commas_from_list(dirs_list)
    names = []
    for elem in dirs_list:
        names.append(str(elem.text))

    return names


def get_genres(cell_soap):
    """Input: a cell soap movie from IMDB;
    output: movie list of genres"""

    genres = []
    movie_genres = cell_soap.find('span', {'class': 'genre'})
    for genre in movie_genres:
        try:
            genres.append(str(genre.text))
        except AttributeError:
            # print 'type is wrong', genre
            continue

    return genres


def get_runtime(cell_soap):
    """Input: a cell soap movie from IMDB;
    output: movie runtime"""

    runtime = cell_soap.find('span', {'class': 'runtime'})
    return str(runtime.text)


def get_certificate(cell_soap):
    """Input: a cell soap movie from IMDB;
    output: movie rating (PG-13, etc.)"""

    try:
        rating = cell_soap.find('span', {'class': 'certificate'})
        return rating.span.get('title')

    except AttributeError:
        rating = np.nan
        return rating


def list_to_dict(movies_list):
    """Give a list of soap objects; return a dictionary"""

    # c4 = movies_list[26]
    # cells = c4.findAll('td')

    movie_dict = {}

    for movie_cell in movies_list:
        cells = movie_cell.findAll('td')
        rank = str(cells[0].find(text=True))

        movie = cells[2]

        money = np.nan
        if len(movie) > 3:
            money = str(cells[3].find(text=True))

        title = get_title(movie)
        print title
        link = get_link(movie)
        year = get_year(movie)
        rating = get_user_rating(movie)
        voters = get_num_voters(movie)
        (dirs, acts) = get_directors_and_actors_list(movie)
        dir_names = directors_names(dirs)
        act_names = directors_names(acts)
        genres = get_genres(movie)
        runtime = get_runtime(movie)
        certificate = get_certificate(movie)

        movie_dict[title] = [rank, money, link, year, rating, voters,
                             dir_names, act_names, genres, runtime,
                             certificate]

    return movie_dict  # , movie


if __name__ == '__main__':
    firefox = webdriver.Firefox()
    # firefox.get("http://www.imdb.com/search/"
    #             "title?at=0&sort=moviemeter&title_type=documentary")

    # I think I need a while loop here...

    firefox.get('http://www.imdb.com/search/'
                'title?at=0&sort=boxoffice_gross_us&title_type=documentary')

    movies = movies_list(firefox.current_url)
    movie_dict = list_to_dict(movies)
    # click_next(firefox)
    # firefox.close()

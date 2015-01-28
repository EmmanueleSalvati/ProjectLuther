"""Module that contains utility functions to scrape IMDB data"""

from selenium import webdriver
import re
import urllib2
from bs4 import BeautifulSoup
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('latin-1')
from time import sleep
import pickle as pkl
import pandas as pd


def click_next(buttons):
    """Find the Next button and click it"""
    # firefox = webdriver.Firefox()
    # firefox.get("http://www.imdb.com/search/"
    #             "title?at=0&sort=moviemeter&title_type=documentary")

    prev_next = buttons.find_elements_by_tag_name('a')
    for button in prev_next:
        next_string_u = button.text
        if re.match('Next', next_string_u):
            print 'Changing page...'
            button.click()
            break
        else:
            continue
    # print len(prev_next)
    return prev_next


def movies_list(url):
    """Input: current url; output the list of movies"""

    page = urllib2.urlopen(url)
    soap = BeautifulSoup(page)
    movies = soap.findAll(class_='even detailed')
    movies.extend(soap.findAll(class_='odd detailed'))

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

    try:
        rating = cell_soap.find('span', {'class': 'rating-rating'})
        return str(rating.span.text)

    except AttributeError:
        return np.nan


def get_num_voters(cell_soap):
    """Input: a cell soap from IMDB; output: movie number of voters"""

    try:
        rating = cell_soap.div.div.get('title')
        full_string = rating.split()

        return full_string[4].replace('(', '').replace(',', '')
    except AttributeError:
        return np.nan


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

    if not movie_credits:
        return float('nan'), float('nan')

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
    if not movie_genres:
        return np.nan
    for genre in movie_genres:
        try:
            genres.append(str(genre.text))
        except AttributeError:
            continue

    return genres


def get_runtime(cell_soap):
    """Input: a cell soap movie from IMDB;
    output: movie runtime"""

    try:
        runtime = cell_soap.find('span', {'class': 'runtime'})
        return str(runtime.text)

    except AttributeError:
        runtime = np.nan
        return runtime


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

    movie_dict = {}

    for movie_cell in movies_list:
        cells = movie_cell.findAll('td')
        rank = str(cells[0].find(text=True))

        movie = cells[2]

        money = np.nan
        if len(cells) > 3:
            money = str(cells[3].find(text=True))

        title = get_title(movie)
        # print title
        link = get_link(movie)
        year = get_year(movie)
        rating = get_user_rating(movie)
        voters = get_num_voters(movie)
        (dirs, acts) = get_directors_and_actors_list(movie)
        try:
            dir_names = directors_names(dirs)
        except TypeError:
            print 'no directors'
            dir_names = np.nan
        try:
            act_names = directors_names(acts)
        except TypeError:
            act_names = np.nan
        genres = get_genres(movie)
        runtime = get_runtime(movie)
        certificate = get_certificate(movie)

        movie_dict[title] = [rank, money, link, year, rating, voters,
                             dir_names, act_names, genres, runtime,
                             certificate]

    return movie_dict  # , movie


def get_IMDB_list(url=None):
    """returns a list of dictionaries
    IMDB link hardocoded here"""

    firefox = webdriver.Firefox()

    # firefox.get("http://www.imdb.com/search/"
    #             "title?at=0&sort=moviemeter&title_type=documentary")

    if url:
        firefox.get(url)
    else:
        firefox.get('http://www.imdb.com/search/'
                    'title?at=0&sort=boxoffice_gross_us&title_type='
                    'documentary')
    print firefox
    all_movies_list = []

    buttons = firefox.find_element_by_class_name('pagination')
    prev_next = buttons.find_elements_by_tag_name('a')
    movies = movies_list(firefox.current_url)
    movie_dict = list_to_dict(movies)
    all_movies_list.append(movie_dict)
    click_next(buttons)
    sleep(3)
    print firefox.current_url
    buttons = firefox.find_element_by_class_name('pagination')
    prev_next = buttons.find_elements_by_tag_name('a')

    counter = 0
    while len(prev_next) == 2 and counter < 20:
        movies = movies_list(firefox.current_url)
        movie_dict = list_to_dict(movies)
        all_movies_list.append(movie_dict)
        counter += 1
        click_next(buttons)
        sleep(3)
        print firefox.current_url
        buttons = firefox.find_element_by_class_name('pagination')
        prev_next = buttons.find_elements_by_tag_name('a')

    last_url = firefox.current_url
    firefox.close()

    return all_movies_list, last_url


def unpack_movie_list(movie_list):
    """Takes a list of dictionaries and returns one big dictionary"""

    movie_dict = {}
    for movies in movie_list:
        movie_dict.update(movies)

    return movie_dict


def create_intermediate_pickles():
    """Loops over all the pages and returns a pickle file for every 20 pages,
    i.e. every 20 * 50 movies"""

    # url = ('http://www.imdb.com/search/'
    #        'title?at=0&sort=boxoffice_gross_us&title_type='
    #        'documentary')

    url = ('http://www.imdb.com/search/'
           'title?at=0&sort=boxoffice_gross_us&start=17901&title_type='
           'documentary')

    for i in range(17, 182):
        with open('IMDB_%s.pkl' % i, 'w') as pklfile:
            movies_list, url = get_IMDB_list(url)
            movies = unpack_movie_list(movies_list)
            pkl.dump(movies, pklfile)


def get_pickles(directory):
    """From a directory, returns a big fat dictionary of movies"""

    big_fat_movie_dict = {}
    import os
    pickle_list = os.listdir(directory)
    pickle_list.remove('IMDB_24.pkl')
    pickle_list.remove('urls_documentaries.pkl')
    pickle_list.remove('urls_political_documentaries.pkl')
    pickle_list.remove('BoxOfficeMojo_documentaries_DataFrame.pkl')
    pickle_list.remove('BoxOfficeMojo_political_documentaries_DataFrame.pkl')

    for IMDBfile in pickle_list:
        with open(str(directory) + str(IMDBfile)) as pklfile:
            tmp_dict = pkl.load(pklfile)
            big_fat_movie_dict.update(tmp_dict)

    return big_fat_movie_dict


##### DataFrame-related functions
def dict_to_dataframe(movie_dict):
    """Input: IMDB movies dictionary; it returns a pandas data frame"""

    movies = pd.DataFrame.from_dict(movie_dict, orient='index')
    movies.columns = ['Rank', 'TotalGross', 'IMDBLink', 'RelYear',
                      'UsersRating', 'NumVoters', 'Directors', 'Actors',
                      'Genres', 'RunTime', 'Rated']

    return movies


def str_to_dollars(pd_series):
    """Transform money to floats"""

    dollars = []
    for elem in pd_series:
        if type(elem) == str and '$' in elem and 'K' in elem:
            elem = float(elem.replace('$', '').replace('K', ''))
        elif type(elem) == str and '$' in elem and 'M' in elem:
            elem = float(elem.replace('$', '').replace('M', ''))
            elem = 1000 * elem
        elif type(elem) == str and '$' in elem:
            elem = float(elem.replace('$', ''))
            elem = elem / 1000
        elif type(elem) == str and '-' in elem:
            elem = np.nan
        dollars.append(elem)

    return dollars


def str_to_year(pd_series):
    """Transorms year to int"""

    years = []
    for elem in pd_series:
        if not elem.isdigit():
            elem = np.nan
        else:
            elem = int(elem)
        years.append(elem)

    return years


def str_to_ratings(pd_series):
    """Transforms rating to float"""

    ratings = []
    for elem in pd_series:
        if type(elem) == str and '.' not in elem:
            elem = np.nan
        elif type(elem) == str and '.' in elem:
            elem = float(elem)
        elif elem != elem:
            elem = np.nan
        ratings.append(elem)

    return ratings


def str_to_voters(pd_series):
    """Transforms voters to int"""

    voters = []
    for elem in pd_series:
        if type(elem) == str and elem.isdigit():
            elem = int(elem)
        elif type(elem) == str and not elem.isdigit():
            elem = np.nan
        elif elem != elem:
            elem = np.nan
        voters.append(elem)

    return voters


def str_to_rank(pd_series):
    """Transforms Rank to int"""

    rank = []
    for elem in pd_series:
        if type(elem) == str and '.' in elem:
            elem = int(float(elem))
        elif elem != elem:
            elem = np.nan
        rank.append(elem)

    return rank


def str_to_runtime(pd_series):
    """Transforms RunTime to int"""

    rtime = []
    for elem in pd_series:
        if type(elem) == str and 'mins.' in elem:
            elem = elem.replace(' mins.', '')
            elem = int(float(elem))
        elif elem != elem:
            elem = np.nan
        rtime.append(elem)

    return rtime

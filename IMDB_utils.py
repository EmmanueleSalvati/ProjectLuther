"""Module that contains utility functions to scrape IMDB data"""

from selenium import webdriver
import re
import urllib2
from bs4 import BeautifulSoup


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
    print len(movies)
    return movies


def get_title(cell_soap):
    """Input: a cell soap from IMDB; output: movie title"""

    title = cell_soap.find('a')
    return str(title.text)


def get_link(cell_soap):
    """Input: a cell soap from IMDB; output: movie IMDB link"""

    link = cell_soap.find('a')
    return link.get('href')


# NEED TO FIX THIS ONE
def get_user_rating(cell_soap):
    """Input: a cell soap from IMDB; output: movie user rating"""

    # ratings = cell_soap.div.find_all('span', {'class': 'rating-rating'})
    rating = cell_soap.div.div.get('title')
    full_string = rating.split()

    return full_string[3]
    # for rating in ratings:
    #     print rating.text
    # return rating


def get_num_voters(cell_soap):
    """Input: a cell soap from IMDB; output: movie number of voters"""

    rating = cell_soap.div.div.get('title')
    full_string = rating.split()

    return full_string[4].replace('(', '').replace(',', '')


def get_directors(cell_soap):
    """Input: a cell soap from IMDB; output: movie list of directors"""




def list_to_dict(movies_list):
    """Give a list of soap objects; return a dictionary"""

    c4 = movies_list[0]
    movie_dict = {}
    cells = c4.findAll('td')
    rank = str(cells[0].find(text=True))

    movie = cells[2]
    title = get_title(movie)
    link = get_link(movie)
    rating = get_user_rating(movie)
    voters = get_num_voters(movie)
    movie_dict[title] = [rank, link, rating, voters]

    return movie_dict, movie


if __name__ == '__main__':
    firefox = webdriver.Firefox()
    firefox.get("http://www.imdb.com/search/"
                "title?at=0&sort=moviemeter&title_type=documentary")

    movies = movies_list(firefox.current_url)
    tmp_cell, movie = list_to_dict(movies)
    # click_next(firefox)

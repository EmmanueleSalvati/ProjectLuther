#!/usr/bin/python
"""
Irmak Sirer, 2013

Python Wrapper around the Google API for search

It returns results for a google search.
A result is a dictionary (json) with the following fields:

cacheUrl
content
title
titleNoFormatting
unescapedUrl
url
visibleUrl

"""

import json
import urllib



class TooManySearchesError(Exception):
    pass

class GoogleSearch(object):
    
    api_url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'

    def __init__(self, query):
        self.query = query
        self._ajax_query = urllib.urlencode({'q': self.query})
        self._result_data = None

    @property
    def result_data(self):
        if self._result_data is None:
            query_url = self.api_url % self._ajax_query
            search_response = urllib.urlopen(query_url).read()
            self._result_data = json.loads(search_response)['responseData']
        if self._result_data is None:
            msg = "You made too many searches in succession, google did not return results."
            raise TooManySearchesError(msg)
        else:
            return self._result_data

    def count(self):
        "Number of results"
        return self.result_data['cursor']['estimatedResultCount']

    def top_result(self):
        """ First hit (what "I'm feeling lucky" would return)"""
        return self.result_data['results'][0]

    def top_results(self):
        """ Top hits (only four by default) """
        return self.result_data['results']

    def top_url(self):
        """ URL of the first hit """
        return self.top_result()['url']

    def top_unescaped_url(self):
        """ unescaped URL of the first hit """
        return self.top_result()['unescapedUrl']

    def top_urls(self):
        """ URLs of the top hits """
        get_url = lambda result: result['url']
        return map(get_url, self.top_results())



#### TESTS AND EXAMPLE USES #########

def get_movie_url_from_bomojo(query):
    query = 'site:boxofficemojo.com ' + query
    gs = GoogleSearch(query)
    first_page = gs.top_result()
    return first_page['url']

def print_top_results(query):
    """ Print a list of top hits for a query. 
    Gives a good idea of what's returned by the api"""
    from pprint import pprint
    gs = GoogleSearch(query)
    for hit in gs.top_results():
        pprint(hit)
        print
    print '------------------\n'


def search_wikipedia(query):
    """Query Wikipedia and show the top hit"""
    gs = GoogleSearch("wikipedia.com: %s" % query)
    print gs.top_result()['titleNoFormatting']
    print gs.top_url()
    print '\n------------------\n'
    return gs.top_url()


def x_vs_y_count_match(x, y):
    """ Which of two words is used 
    more on the Internet?"""
    nx = int(GoogleSearch(x).count())
    ny = int(GoogleSearch(y).count())
    print '%s vs %s:' % (x,y)
    if   nx > ny:
        print '%s wins with %i vs %i' % (x,nx,ny)
    elif nx < ny:
        print '%s wins with %i vs %i' % (y,ny,nx)
    else:
        print "it's a tie with %s each!" % nx
    print '\n------------------\n'
    return nx, ny


def imdb_id_for_movie(movie_name):
    """Retrieve the imdb id for a movie 
    from the name (and year if there are remakes)"""
    query = 'imdb.com: %s' % movie_name
    url = GoogleSearch( query ).top_url()
    import re
    imdb_id = re.search('/tt[0-9]+/', url).group(0).strip('/')
    print 'The imdb id for %s is %s' % (movie_name, imdb_id)
    print '\n------------------\n'
    return imdb_id


# Apply the tests/examples
if __name__ == '__main__':

    ##### EXAMPLE 1: Top Results for a query #####
    print_top_results("Bacon")

    ##### EXAMPLE 2: Search Wikipedia (first hit) #####
    search_wikipedia("Porcupine")

    ##### EXAMPLE 3: Which is used more, "color" or "colour"? #####
    x_vs_y_count_match("color", "colour")

    ##### EXAMPLE 4: Retrieve imdb id of a movie #####
    imdb_id_for_movie("Total Recall 1990")

    ##### EXAMPLE 5: Search google to find the box office mojo page url for a movie
    print get_movie_url_from_bomojo("Dawn of the Planet of the Apes 2014")

    

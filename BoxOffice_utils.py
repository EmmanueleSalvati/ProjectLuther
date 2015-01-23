"""Module that contains utility functions to scrape BoxOfficeMojo data"""
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys


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
        links_dict[movies_range] = 'http://boxofficemojo.com' + href

    return links_dict

"""This is the main file to run to scrape movies"""

import sys
sys.path.append('/Users/JerkFace/Metis/Projects/Luther/')

import BoxOffice_utils
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
    ARGS = sys.argv[1:]

    url_dict_pkl = ARGS[0]
    dataframe_pkl = ARGS[1]

    movie_dict = BoxOffice_utils.get_all_movies(url_dict_pkl)
    movies_df = BoxOffice_utils.dict_to_dataframe(movie_dict)
    with open(dataframe_pkl, 'w') as pklfile:
        pkl.dump(movies_df, pklfile)

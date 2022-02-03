from datetime import datetime

import urllib3
from bs4 import BeautifulSoup

year = datetime.today().year
YEARS = [year - i for i in range(30)]
COUNTRIES = ['fi', 'ru']


def get_top_one_movie_by_year_and_country(year, country):
    url = (
        'https://www.imdb.com/search/title/'
        + '?release_date={year}&countries={country}&count=1'.format(
            year=year,
            country=country
        )
    )
    html = urllib3.PoolManager().request('GET', url).data
    soup = BeautifulSoup(html, 'lxml')
    movie_list = soup.findAll('div', attrs={'class': 'lister-item-content'})

    for movie in movie_list:
        header = movie.findChildren(
            'h3', attrs={'class': 'lister-item-header'}
        )
        muted_text = movie.findChildren('p', attrs={'class': 'text-muted'})
        ratings_bar = movie.findChildren('div', attrs={'class': 'ratings-bar'})

        title = header[0].findChildren('a')[0].contents[0]
        genre = muted_text[0].findChildren(
            'span', attrs={'class': 'genre'}
        )[0].contents[0].replace('\n', '').rstrip()
        rate_str = ratings_bar[0].findChildren(
            'div', attrs={'class': 'inline-block ratings-imdb-rating'}
        )

        if rate_str:
            rate = rate_str[0].find('strong').text
        else:
            rate = '-.-'

        print(f'\t{country} : {rate} | {title} | {genre}')


def get_top_one_movie_by_year(year):
    for country in COUNTRIES:
        get_top_one_movie_by_year_and_country(year, country)


for year in YEARS:
    print(f'{year}:')
    get_top_one_movie_by_year(year)
    print('-'*80)

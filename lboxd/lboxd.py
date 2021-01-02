#!/bin/env python3

'''
Letterboxd does not really have an API.
Test account:
    testfitzy1293
'''


import requests
import sys
import re
from bs4 import BeautifulSoup
from pprint import pprint
import json
from time import time
from time import sleep, time
from webbrowser import open_new_tab
import argparse
from rich.console import Console
from rich import print as rprint

from .utils import *


#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************

console = Console()
movieDelim = f'[red]{"=" * 80}'

if len(sys.argv) > 1:
    parser = argparse.ArgumentParser(description='letterboxd args')
    parser.add_argument('--user', '-u', dest='user', help='letterboxd.com user')
    parser.add_argument('--reviews', '-r', dest='reviews', action="store_true", default=False, help='Gets reviews')
    parser.add_argument('--testing', '-t', dest='testing', action='store_true', default=False, help='Testing flag - for development only')
    parser.add_argument('--save-json', '-j', dest='json', action="store_true", default=False, help='Saves a JSON file of the reviews dictionary')
    parser.add_argument('--save-html', '-w', dest='html', action="store_true", default=False, help='Saves an HTML document for easily viewing reviews')
    parser.add_argument('--browser-open', '-b', dest='browserOpen', action="store_true", default=False, help='Opens saved HTML document in the browser')
    parser.add_argument('--search', '-s', nargs='+', dest='search', default=())
    args = parser.parse_args()
else:
    args = None

#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************

def searchMovie(user=''):
    reviewsText = {}
    if args.search:
        console.print(movieDelim)
        for url in [f'https://letterboxd.com/{user}/film/{movie}/' for movie in args.search]:
            movie = url.split('/film/')[-1][:-1]
            console.print(f'[cyan]movie: [bold blue]{movie}')
            console.print(f'\t[green]Searching')
            console.print(f'\t[green]Requesting: {url}')
            console.print(movieDelim)

            reviewsText[movie] = getSingleReview(url=url, args=args)
        return reviewsText

#~~~=======================================================================================================================================================================


#A mess. For the CLI 
def getReviews(user, args=''):
    url = f'https://letterboxd.com/{user}/films/reviews'
    reviewsText = {}
    previewChar = '…' #NOT THREE PERIODS - DIFFERENT UNICODE CHAR
    titleStr = f'<a href="/{user}/film/'
    session = requests.session()

    console.print('[cyan] Urls with multiple reviews')
    start = time()
    reviewUrls = getReviewUrls(url=url, session=session)
    rprint(reviewUrls)
    rprint(f'reponseTime={time() - start}\n')

    console.print(movieDelim)
    for url in reviewUrls:
        console.print(f'[cyan]Requesting: [bold blue]{url}')
        start = time()
        htmlText = getHtmlText(url=url, session=session)
        rprint(f'reponseTime={time() - start}')
        console.print(movieDelim)


        soup = BeautifulSoup(htmlText, 'html.parser')
        for topDiv in soup.find_all('div', {'class':"film-detail-content"}):
            movie = str(topDiv.find('a')).replace(titleStr, '').split('/')[0]
            reviewPreview = str(topDiv.find('div', {'class': 'body-text -prose collapsible-text'}).find_all('p'))[1:-1]
            reviewPreview = reviewPreview.replace('</p>,', '</p>')

            console.print(f'[cyan]movie: [bold blue]{movie}')

            if reviewPreview[-5] == previewChar:
                movieReviewUrl = f'https://letterboxd.com/{user}/film/{movie}/'
                console.print('\t[magenta]Preview contains partial review')
                console.print(f'\t[magenta]Requesting: {movieReviewUrl}')

                start = time()
                reviewsText[movie] = getSingleReview(url=movieReviewUrl, session=session)
                rprint(f'\treponseTime={time() - start}')
                console.print(movieDelim)

            else:
                console.print('\t[blue]Preview contains full review')
                console.print('\t[blue]No need to request individual page')
                console.print(movieDelim)

                reviewsText[movie] = reviewPreview

    return reviewsText

#~~~=======================================================================================================================================================================

def writeReviews(reviewsDict={}, args=''):
    user = reviewsDict['user']
    if not args.search:
        fname = f'{user}_all_reviews.html'

    else:
        fname = f'{user}_searched_reviews.html'
    rprint(f'html={fname}')

    with open(fname, 'w+') as f:
        f.write(
            '<!DOCTYPE html>\n'
            '<html>\n'
            '<head>\n'
            '</head>\n'
            '<body>\n'
        )

        f.write(f'<h1>{user} - letterboxd.com reviews </h1>\n<br>\n')

        for i, (movie, review) in enumerate(reviewsDict['reviews'].items()):
            htmlMovieTitle = movie.replace('-', ' ').title()
            f.write(f'<b>{i + 1}: {htmlMovieTitle}</b>\n<br>\n{review}\n<br>\n')

        f.write('</body>\n</html>\n')

    if args.browserOpen:
        open_new_tab(fname)

#~~~=======================================================================================================================================================================

def letterboxdRun():
    if args.testing:
        args.reviews = True
        args.html = True
        user = 'testfitzy1293'
    else:
        user = args.user

    if args.reviews:
        fname = f'{user}_reviews.json'
        console.print('[cyan]--Making requests to letterboxd.com--\n[red]This may take some time depending on how many reviews there are.\n')

        reviewsText = getReviews(user, args=args)

        outputDict = {'user': user, 'reviews': reviewsText}

        if args.html:
            writeReviews(outputDict, args=args)
        if args.json:
            rprint(f'json={fname}')
            jsonStr = json.dumps(outputDict, indent=3)
            with open(fname, 'w+') as f:
                f.write(jsonStr)

#~~~=======================================================================================================================================================================

def main():
    if args is not None:
        argsDict = vars(args)

        console.print('[cyan]*Command line arguments* ')
        for k,v in argsDict.items():
            rprint(f'\t{k}={v}')
        print()

        letterboxdRun()

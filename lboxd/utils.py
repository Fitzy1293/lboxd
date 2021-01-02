import requests
from bs4 import BeautifulSoup
from rich import print as rprint
from time import time
from pprint import pprint
from collections import defaultdict


starChar = '★'
halfChar = '½'
previewChar = '…'
def getHtmlText(url='', session=''):

    httpGet = session.get(url).text
    return httpGet

#~~~=======================================================================================================================================================================

def getSingleReview(url='', args='', session=''):
    for possibleUrl in (url, url + '/1/'): # super-8 review had a an extra /1/ on the end
        soup = BeautifulSoup(getHtmlText(url=possibleUrl, session=session), 'html.parser')
        reviewDivHtmlStr = soup.find("div", {'class': "review body-text -prose -hero -loose"})
        if not reviewDivHtmlStr  == None:
            returnStr = str(reviewDivHtmlStr).split('<div><p>')[-1].replace('</div>', '')
            return f'<p>{returnStr}'

#~~~=======================================================================================================================================================================

def getReviewUrls(user='', session='', url=''):
    url = url.strip('/')

    htmlText = getHtmlText(url=url, session=session)
    soup = BeautifulSoup(htmlText, 'html.parser')
    pageDiv = str(soup.find("div", {'class': "pagination"}))
    try:
        lastValidPage = int(pageDiv.split('/page/')[-1].split('/')[0])

        return [f'{url}/page/{str(i)}' for i in range(1, lastValidPage + 1)]

    except ValueError:

        return [f'{url}/page/1']

#~~~=======================================================================================================================================================================

def reviews(user='', url='', session='', count=None):
    reviewPagesUrl = f'https://letterboxd.com/{user}/films/reviews'
    if session == '':
        session = requests.session()

    ct = 0
    for url in getReviewUrls(url=reviewPagesUrl, session=session):
        htmlText = getHtmlText(url=url, session=session)

        soup = BeautifulSoup(htmlText, 'html.parser')

        for topDiv in soup.find_all('div', {'class':"film-detail-content"}):
            if ct == count:
                return
            ct+=1

            movie = str(topDiv.find('a')).replace(f'<a href="/{user}/film/', '').split('/')[0]
            reviewPreview = str(topDiv.find('div', {'class': 'body-text -prose collapsible-text'}).find_all('p'))[1:-1]
            reviewPreview = reviewPreview.replace('</p>,', '</p>')

            if reviewPreview[-5] == previewChar:
                movieReviewUrl = f'https://letterboxd.com/{user}/film/{movie}/'
                yield {'title': movie, 'review': getSingleReview(url=movieReviewUrl, session=session)}

            else:
                yield {'title': movie, 'review': reviewPreview}



#~~~=======================================================================================================================================================================

def lboxdlist(user='', onlyRated=False, count=None):
    url = f'https://letterboxd.com/{user}/films'
    reviewUrl = f'https://letterboxd.com/{user}/films/reviews'
    singleUrl = url[:-1]
    titleStr = 'data-film-slug="/film/'

    session = requests.session()

    titleRating = {}
    ct = 0
    for url in getReviewUrls(user=user, session=session, url=url):
        htmlText = getHtmlText(url=url, session=session)
        soup = BeautifulSoup(htmlText, 'html.parser')

        for topDiv in soup.find_all('ul', {'class':"poster-list -p70 -grid film-list clear"}):
            movies = [(i.split('/')[0], f'{i.count(starChar) + i.count(halfChar) / 2}'.replace('0.0', '')) for i in str(topDiv).split(titleStr) if i[0] != '<']

        if onlyRated:
            movies = [i for i in movies if i[1] != '']

        for movie in movies:
            if ct == count:
                return
            ct+=1
            yield {'title':movie[0], 'rating': movie[1]}








#~~~=======================================================================================================================================================================

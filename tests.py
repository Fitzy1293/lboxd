import lboxd
from bs4 import BeautifulSoup as bs
from rich import print as rprint
from lboxd import lboxdlist

fitz = 'testfitzy1293'
rlm = 'redlettermedia'

def simpleTests():
    tester = rlm

    rprint('purpose=all_movies')
    for movie in lboxd.lboxdlist(user=tester):
        rprint(movie)

    checking = 10
    rprint(f'purpose=only_{checking}_movies')
    for movie in lboxd.lboxdlist(user=tester, count=checking):
        rprint(movie)

    print()

def prettyHtmlTest():
    tester = rlm
    checking = 5

    for review in lboxd.reviews(user=tester, count=checking):
        title = review ['title']
        review = review['review']
        htmlPretty = bs.prettify(bs(review, 'html.parser'))

        rprint(f'[yellow]Title:[/yellow] [red]{title}[/red]\n{htmlPretty}')

    print()

def movieListTest():
    tester = 'daqoon'

    for review in lboxdlist(user=tester):
        title = review ['title']
        rating = review['rating']
        richTitle = f'[yellow]Title:[/yellow] [red]{title}[/red]'

        if rating:
            rprint(f'{richTitle} rating={rating}')
        else:
            rprint(richTitle)

    print()

def runTests():
    prettyHtmlTest()
    movieListTest()
    simpleTests()
    print('\nDONE')

runTests()

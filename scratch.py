import lboxd
from pprint import pprint
from statistics import mean
from rich import print as rprint
import sys
from rich.console import Console
from bs4 import BeautifulSoup as bs

console = Console()

testUser = 'testfitzy1293'
lotsOfReviewsUser = 'pd187'
rlm = 'redlettermedia'
ty = 'daqoon'

def testMain():
    lboxd.main()
    sys.exit()



reviewExample()
#testMain()

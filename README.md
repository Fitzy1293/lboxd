
# lboxd <br> An unofficial letterboxd.com API

Get reviews from letterboxd users. Done with pure HTML parsing.

## Development Environment

- Ubuntu 20.04 lts

- Python 3.8.5

This has not been tested on Windows, there may be encoding problems.


# Installation

`pip install lboxd`

# Usage
```py
'''
Pretty printing reviews with a generator.
    => Generators are good for when there are requests to many different URLs.
    => A new requests session is created for the duration of the generator.
'''

import lboxd
from bs4 import BeautifulSoup as bs
from rich import print as rprint

for review in lboxd.reviews(user='redlettermedia', count=5):
    title = review ['title']
    review = review['review']
    htmlPretty = bs.prettify(bs(review, 'html.parser'))

    rprint(f'[yellow]Title:[/yellow] [red]{title}[/red]\n{htmlPretty}')
```

![Redlettermedia example](https://i.imgur.com/fejIZoR.png)


```py
from lboxd import lboxdlist
from rich import print as rprint

for movie in lboxdlist(user='daqoon'):
    title = movie ['title']
    rating = movie['rating']
    richTitle = f'[yellow]Title:[/yellow] [red]{title}[/red]'

    if rating:
        rprint(f'{richTitle} rating={rating}')
    else:
        rprint(richTitle)
```


![Redlettermedia example](https://i.imgur.com/YXjwaN9.png)



# CLI

## Example

![Redlettermedia example](https://i.imgur.com/34XaBY0.png)


## Arguments

  `--user USER` `-u USER`   letterboxd.com user

  `--reviews` `-r`          Gets reviews

  `--testing` `-t`          Testing flag - for development only

  `--save-html` `-w`          Saves an HTML document for easily viewing reviews

  `--browser-open` `-b`        Opens saved HTML document in the browser

  `--search SEARCH [SEARCH ...]` `-s SEARCH [SEARCH ...]` Will only get search terms, currently needs to match exactly with letterboxd notation. Replace spaces with dashes.  

import requests
import bs4

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

'''This code finds all the unique authors in https://quotes.toscrape.com , the website has
multiple pages which are being iterated till the end by a common method which can usually be used for
other websites too'''

# value initialized for the while loop.
C = 1
# lst initialized as an empty set.
# used set instead of list as there are multiple quotes by a single author.
lst = set()

# divided the url into two parts to map to the next page(one of many ways).
add_url = '/page/1/'
base_url = 'https://quotes.toscrape.com'

# StackOverflow code not much idea about how it works;links:
# https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests
# https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request

# StackOverflow start:
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
# StackOverflow end.

# while loop to traverse through the pages
while C:

    # changed requests to session
    res = session.get(base_url + add_url)
    soup = bs4.BeautifulSoup(res.content, 'lxml')

    # value initialized for 2^nd while loop.
    C1 = 1
    # value initialized for iterating through the list returned by select().
    i = 0

    # 2^nd while loop to traverse through each author name in current page.
    while C1:
        try:
            # reaching the end of objects with class = author gives an IndexError which
            # can be used to denote the end of 2^nd while loop.
            lst.add(soup.select('.author')[i].text)
            i += 1
        except IndexError:
            C1 = 0

    try:
        # reaching the end of objects with class = next and tag = <a> will give an IndexError which
        # can be used to denote the end of while loop.
        # index[0] is used even though it only has a single object as select() returns a list
        # which cannot be used to access '/page/(num)' using ['href'] key,
        # whereas the list elements are bs4.element.Tag objects.
        add_url = soup.select('.next a')[0]['href']
    except IndexError:
        C = 0

print(lst)

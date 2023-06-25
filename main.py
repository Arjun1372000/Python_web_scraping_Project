import requests
import bs4

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

C = 1
lst = set()
add_url = '/page/1/'
base_url = 'https://quotes.toscrape.com'
# StackOverflow code not much idea about how it works.
# https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests
# https://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
# StackOverflow start
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
# StackOverflow end

while C:
    # changed requests to session
    res = session.get(base_url + add_url)
    soup = bs4.BeautifulSoup(res.content, 'lxml')

    C1 = 1
    i = 0
    while C1:
        try:
            lst.add(soup.select('.author')[i].text)
            i += 1
        except IndexError:
            C1 = 0

    try:
        add_url = soup.select('.next a')[0]['href']
    except IndexError:
        C = 0

print(lst)

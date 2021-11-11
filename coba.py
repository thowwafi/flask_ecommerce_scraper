import cloudscraper
from bs4 import BeautifulSoup

# Adding Browser / User-Agent Filtering should help ie. 

# will give you only desktop firefox User-Agents on Windows
scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})

res = scraper.get("https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth")
import pdb; pdb.set_trace()
html = res.content

soup = BeautifulSoup(html, 'html.parser')

print(soup)
# import os
# from tbselenium.tbdriver import TorBrowserDriver

# root_path = os.getcwd()
# GECKODRIVER_PATH = os.path.join(root_path, "geckodriver")
# with TorBrowserDriver(executable_path=GECKODRIVER_PATH) as driver:
#     driver.get('https://check.torproject.org')
#     print(driver.page_source)
url = "https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth"

import cloudscraper

scraper = cloudscraper.create_scraper()
print(scraper.get(url).text) 
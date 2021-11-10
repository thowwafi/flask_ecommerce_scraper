import undetected_chromedriver.v2 as uc
from pprint import pformat

driver = uc.Chrome(enable_cdp_events=True)

def mylousyprintfunction(eventdata):
    print("pformat(eventdata)", pformat(eventdata))

# for more inspiration checkout the link below
# https://chromedevtools.github.io/devtools-protocol/1-3/Network/

# and of couse 2 lousy examples
driver.add_cdp_listener('*', mylousyprintfunction)

# hint: a wildcard captures all events!
# driver.add_cdp_listener('*', mylousyprintfunction)

# now all these events will be printed in my console
url = "https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth"
# with driver:
driver.get(url)
import pdb; pdb.set_trace() 
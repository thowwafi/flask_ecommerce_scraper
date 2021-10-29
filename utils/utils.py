import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def sleep_time(number):
    for i in range(number, 0, -1):
        print(f"{i}", end='\n', flush=True)
        time.sleep(1)

def makeDirIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def initialize_webdriver(root_path):
    CHROMEDRIVER_PATH = os.path.join(root_path, "chromedriver")
    try:
        options = Options()
        # options.add_argument("--headless")
        options.add_argument('window-size=1920x1080')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        return webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options), "Ok"
    except OSError:
        return None, "Chrome webdriver not matching with OS"
    except Exception as e:
        return None, e

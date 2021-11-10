import os
import time
from selenium import webdriver
from seleniumwire import webdriver as seleniumwire_webdriver
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.firefox.options import Options as FOptions


def sleep_time(number):
    for i in range(number, 0, -1):
        print(f"{i}", end='\n', flush=True)
        time.sleep(1)

def makeDirIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def initialize_webdriver(root_path):
    """
    Initialize Mozilla Gecko Driver
    Make sure the geckodriver file is match with OS and Chrome version
    Download link: https://github.com/mozilla/geckodriver/releases
    @root_path: folder path of project
    @return driver and message
    """
    CHROMEDRIVER_PATH = os.path.join(root_path, "chromedriver")
    GECKODRIVER_PATH = os.path.join(root_path, "geckodriver")
    try:
        options = FOptions()
        # options.add_argument("--headless")
        options.add_argument('window-size=1920x1080')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        return webdriver.Firefox(executable_path=GECKODRIVER_PATH, options=options), "Ok"
    except OSError:
        return None, "Mozilla webdriver not matching with OS"
    except Exception as e:
        return None, e


def initialize_webdriver2(root_path):
    """
    Initialize Mozilla Gecko Driver
    Make sure the geckodriver file is match with OS and Chrome version
    Download link: https://github.com/mozilla/geckodriver/releases
    @root_path: folder path of project
    @return driver and message
    """
    CHROMEDRIVER_PATH = os.path.join(root_path, "chromedriver")
    GECKODRIVER_PATH = os.path.join(root_path, "geckodriver")
    try:
        options = seleniumwire_webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        options.add_argument('--window-size=1920x1080')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        return seleniumwire_webdriver.Firefox(executable_path=GECKODRIVER_PATH, options=options), "Ok"
    except OSError:
        return None, "Mozilla webdriver not matching with OS"
    except Exception as e:
        return None, e

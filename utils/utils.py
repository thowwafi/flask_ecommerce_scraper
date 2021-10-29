import os
import time

def sleep_time(number):
    for i in range(number, 0, -1):
        print(f"{i}", end='\n', flush=True)
        time.sleep(1)

def makeDirIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)

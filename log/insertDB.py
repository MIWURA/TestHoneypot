import json
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from func import getDB


counter = 0
def respond_to_client():
    while True:
        global counter
        with open("DBmypot.txt", "r+") as f:
            log_lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in log_lines:
                getDB(line) 
                print(line)
                print("******************")
                print(counter)
                counter += 1
        time.sleep(0.5)


respond_to_client()
from func import getDB
import json
import time

import time

counter = 0
def respond_to_client():
    while True:
        global counter
        with open("DBcowrie.txt", "r+") as f:
            log_lines = f.readlines()
            f.seek(0)
            f.truncate()
            for line in log_lines:
                getDB(line)  # ลบช่องว่างและตัวขึ้นบรรทัดในท้ายของข้อความ
                print(line)
                print("******************")
                print(counter)
                counter += 1
        time.sleep(0.5)

      
respond_to_client()
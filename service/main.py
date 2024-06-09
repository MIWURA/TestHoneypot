import subprocess
import time
import os

# ดึงค่า username ของผู้ใช้ปัจจุบัน
username = os.getlogin()

# รัน reset.py ก่อน
print("Running reset.py...")
subprocess.run(["python", f"/home/{username}/TestHoneypot/log/reset.py"])

# รัน Getcowriedb.py ใน background
print("Running backup.py...")
subprocess.Popen(["python", f"/home/{username}/TestHoneypot/log/backup.py"])

# รัน Getcowriedb.py ใน background
print("Running Getcowriedb.py...")
subprocess.Popen(["python", f"/home/{username}/TestHoneypot/log/Getcowriedb.py"])

# รัน Getdionaeadb.py ใน background
print("Running Getdionaeadb.py...")
subprocess.Popen(["python", f"/home/{username}/TestHoneypot/log/Getdionaeadb.py"])

# รัน insertDB.py ใน background
print("Running insertDB.py...")
subprocess.Popen(["python", f"/home/{username}/TestHoneypot/log/insertDB.py"])

# รัน Flask application
print("Running Flask app.py...")
subprocess.Popen(["python", f"/home/{username}/TestHoneypot/app.py"])

print("All scripts started.")

# Loop to keep the script running
while True:
    time.sleep(60)

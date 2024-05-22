import os
import time
import fcntl
from collections import defaultdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ฟังก์ชั่นในการอ่าน log จากไฟล์ text พร้อมการล็อกไฟล์
def read_log_file(file_path, last_position):
    try:
        with open(file_path, 'r') as file:
            fcntl.flock(file, fcntl.LOCK_SH)  # ล็อกไฟล์สำหรับการอ่าน
            file.seek(last_position)
            lines = file.readlines()
            last_position = file.tell()
            fcntl.flock(file, fcntl.LOCK_UN)  # ปลดล็อกไฟล์
            return lines, last_position
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return [], last_position
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return [], last_position

# ฟังก์ชั่นในการแยก log ตามปี เดือน และวัน
def split_logs_by_year_month_and_day(log_lines):
    logs_by_year_month_and_day = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for line in log_lines:
        if line.startswith('['):
            date_str = line[1:9]  # ดึงวันที่จาก log
            day = date_str[:2]  # ดึงเฉพาะวัน
            month = date_str[2:4]  # ดึงเฉพาะเดือน
            year = date_str[4:8]  # ดึงเฉพาะปี
            logs_by_year_month_and_day[year][month][day].append(line)
    return logs_by_year_month_and_day

# ฟังก์ชั่นในการบันทึก log แยกไฟล์ตามปี เดือน และวัน
def save_logs_by_year_month_and_day(logs_by_year_month_and_day, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for year, months_logs in logs_by_year_month_and_day.items():
        year_directory = os.path.join(output_directory, year)
        if not os.path.exists(year_directory):
            os.makedirs(year_directory)
        for month, days_logs in months_logs.items():
            month_directory = os.path.join(year_directory, month)
            if not os.path.exists(month_directory):
                os.makedirs(month_directory)
            for day, logs in days_logs.items():
                output_file = os.path.join(month_directory, f'{day}{month}{year}.log')
                with open(output_file, 'a') as file:  # เปลี่ยนโหมดเป็น 'a' สำหรับ append
                    file.writelines(logs)

# ฟังก์ชั่นในการเขียนไฟล์ว่างแทนการลบไฟล์ log เก่า
def write_empty_log_file(file_path):
    try:
        with open(file_path, 'w') as file:
            file.write("")
        print(f"Successfully wrote empty log file: {file_path}")
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")

# ฟังก์ชั่นในการตรวจสอบว่าไฟล์ log มีการเปลี่ยนแปลงหรือไม่
def check_log_file_unchanged(file_path, last_position):
    time.sleep(5)  # เว้นระยะเวลา 5 วินาที
    current_position = os.path.getsize(file_path)
    return current_position == last_position

# ตั้งค่า path ของไฟล์ log และ directory สำหรับบันทึกไฟล์ที่แยกตามปี เดือน และวัน
log_file_path = '/opt/dionaea/var/log/dionaea/dionaea.log'
output_directory = '/home/os/TestHoneypot/dionaealogmanagement'
position_file_path = '/home/os/TestHoneypot/last_position.txt'

# ฟังก์ชั่นในการอ่านตำแหน่งสุดท้ายที่อ่านไฟล์
def read_last_position(position_file_path):
    if os.path.exists(position_file_path):
        with open(position_file_path, 'r') as file:
            return int(file.read().strip())
    return 0

# ฟังก์ชั่นในการบันทึกตำแหน่งสุดท้ายที่อ่านไฟล์
def save_last_position(position_file_path, last_position):
    with open(position_file_path, 'w') as file:
        file.write(str(last_position))

# Handler สำหรับการเปลี่ยนแปลงของไฟล์ log
class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == log_file_path:
            print(f"{log_file_path} has been modified")
            last_position = read_last_position(position_file_path)
            log_lines, last_position = read_log_file(log_file_path, last_position)
            if log_lines:
                # แยก log ตามปี เดือน และวัน
                logs_by_year_month_and_day = split_logs_by_year_month_and_day(log_lines)
                # บันทึก log แยกไฟล์ตามปี เดือน และวัน
                save_logs_by_year_month_and_day(logs_by_year_month_and_day, output_directory)
                # บันทึกตำแหน่งสุดท้ายที่อ่านไฟล์
                save_last_position(position_file_path, last_position)
                # เขียนไฟล์ว่างแทนการลบไฟล์ log เก่า
                write_empty_log_file(log_file_path)
                # ตรวจสอบว่าไฟล์ log มีการเปลี่ยนแปลงหรือไม่
                if check_log_file_unchanged(log_file_path, last_position):
                    write_empty_log_file(log_file_path)

if __name__ == "__main__":
    event_handler = LogFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(log_file_path), recursive=False)
    observer.start()
    print(f"Watching for changes in {log_file_path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

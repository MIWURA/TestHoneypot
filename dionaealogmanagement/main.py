import os
from collections import defaultdict

# ฟังก์ชั่นในการอ่าน log จากไฟล์ text
def read_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

# ฟังก์ชั่นในการแยก log ตามปี เดือน และวัน
def split_logs_by_year_month_and_day(log_lines):
    logs_by_year_month_and_day = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for line in log_lines:
        if line.startswith('['):
            date_str = line[1:9]  # ดึงวันที่จาก log
            year = date_str[:4]  # ดึงเฉพาะปี
            month = date_str[4:6]  # ดึงเฉพาะเดือน
            day = date_str[6:8]  # ดึงเฉพาะวัน
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
                output_file = os.path.join(month_directory, f'{year}{month}{day}.log')
                with open(output_file, 'a') as file:  # เปลี่ยนโหมดเป็น 'a' สำหรับ append
                    file.writelines(logs)

# ฟังก์ชั่นในการลบไฟล์ log เก่าหลังจากการแบ่งแยก log
def delete_old_log_file(file_path):
    try:
        os.remove(file_path)
        print(f"Successfully deleted old log file: {file_path}")
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")

# ตั้งค่า path ของไฟล์ log และ directory สำหรับบันทึกไฟล์ที่แยกตามปี เดือน และวัน
log_file_path = '/opt/dionaea/var/log/dionaea/dionaea.log'
output_directory = '/home/os/TestHoneypot/dionaealogmanagement'

# อ่าน log จากไฟล์
log_lines = read_log_file(log_file_path)

# ตรวจสอบว่ามี log ให้อ่านหรือไม่
if log_lines:
    # แยก log ตามปี เดือน และวัน
    logs_by_year_month_and_day = split_logs_by_year_month_and_day(log_lines)

    # บันทึก log แยกไฟล์ตามปี เดือน และวัน
    save_logs_by_year_month_and_day(logs_by_year_month_and_day, output_directory)

    # ลบไฟล์ log เก่า
    delete_old_log_file(log_file_path)

    print("Logs have been successfully split, saved by year, month, and day, and the old log file has been deleted.")
else:
    print("No logs to process.")

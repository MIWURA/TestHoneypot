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

# ฟังก์ชั่นในการแยก log ตามเดือน
def split_logs_by_month(log_lines):
    logs_by_month = defaultdict(list)
    for line in log_lines:
        if line.startswith('['):
            date_str = line[1:9]  # ดึงวันที่จาก log
            year_month = date_str[:6]  # ดึงเฉพาะปีและเดือน
            logs_by_month[year_month].append(line)
    return logs_by_month

# ฟังก์ชั่นในการบันทึก log แยกไฟล์ตามเดือน (เขียนต่อไฟล์เดิม)
def save_logs_by_month(logs_by_month, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for year_month, logs in logs_by_month.items():
        output_file = os.path.join(output_directory, f'{year_month}.log')
        with open(output_file, 'a') as file:  # เปลี่ยนโหมดเป็น 'a' สำหรับ append
            file.writelines(logs)

# ฟังก์ชั่นในการลบไฟล์ log เก่าหลังจากการแบ่งแยก log
def delete_old_log_file(file_path):
    try:
        os.remove(file_path)
        print(f"Successfully deleted old log file: {file_path}")
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")

# ตั้งค่า path ของไฟล์ log และ directory สำหรับบันทึกไฟล์ที่แยกตามเดือน
log_file_path = '/opt/dionaea/var/log/dionaea/dionaea.log'
output_directory = '/home/os/TestHoneypot/dionaealogmanagement'

# อ่าน log จากไฟล์
log_lines = read_log_file(log_file_path)

# ตรวจสอบว่ามี log ให้อ่านหรือไม่
if log_lines:
    # แยก log ตามเดือน
    logs_by_month = split_logs_by_month(log_lines)

    # บันทึก log แยกไฟล์ตามเดือน
    save_logs_by_month(logs_by_month, output_directory)

    # ลบไฟล์ log เก่า
    delete_old_log_file(log_file_path)

    print("Logs have been successfully split, appended to monthly files, and the old log file has been deleted.")
else:
    print("No logs to process.")

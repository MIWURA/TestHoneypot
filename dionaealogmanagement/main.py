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

# ฟังก์ชั่นในการลบไฟล์เก่าใน directory (ไม่จำเป็นต้องใช้ในกรณีนี้)
def clear_output_directory(output_directory):
    if os.path.exists(output_directory):
        for filename in os.listdir(output_directory):
            file_path = os.path.join(output_directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

# ฟังก์ชั่นในการบันทึก log แยกไฟล์ตามเดือน (เขียนต่อไฟล์เดิม)
def save_logs_by_month(logs_by_month, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for year_month, logs in logs_by_month.items():
        output_file = os.path.join(output_directory, f'{year_month}.log')
        with open(output_file, 'a') as file:  # เปลี่ยนโหมดเป็น 'a' สำหรับ append
            file.writelines(logs)

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

    print("Logs have been successfully split and appended to monthly files.")
else:
    print("No logs to process.")

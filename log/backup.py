import os
from datetime import datetime

def categorize_logs_by_date(file_path):
    # Create the base directory for categorized logs
    base_directory = "backup"
    os.makedirs(base_directory, exist_ok=True)
    
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Split the log entry to extract the date
                parts = line.split(', ')
                date_str = parts[2]
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                
                # Create year, month, and day directories
                year_dir = os.path.join(base_directory, date_obj.strftime('%Y'))
                month_dir = os.path.join(year_dir, date_obj.strftime('%m'))
                day_dir = os.path.join(month_dir, date_obj.strftime('%d'))
                
                os.makedirs(day_dir, exist_ok=True)
                
                # Write the log entry to the appropriate file
                log_file_path = os.path.join(day_dir, 'log.txt')
                with open(log_file_path, 'a') as log_file:
                    log_file.write(line)
            except Exception as e:
                print(f"Error processing line: {line}")
                print(f"Error: {e}")

# Usage
file_path = '/home/os/TestHoneypot/log/DBmypot_backup.txt'
categorize_logs_by_date(file_path)

import time
import logging

# ตั้งค่า logging
logging.basicConfig(filename='DBcowrie.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def process_line(line):
    alert = ""
    if line[0] == "[":
        temp = line.split(' ')
        if temp[2] == "log_sqlite" :
            if temp[4] == "accepted" and temp[5] == "connection":
                date = temp[0][1:]
                date = date[4:] + "-" + date[2:][:-4] + "-" + date[:-6]
                time_str = temp[1][:-1]
                ips_temp = temp[9].split(':')
                ipa_temp = temp[7].split(':')
                if ips_temp[1] == "21":
                    alert = "YELLOW!"
                    protocol = "ftp"
                elif ips_temp[1] == "53":
                    alert = "YELLOW!"
                    protocol = "nameserver"
                # เพิ่มเงื่อนไขสำหรับ port อื่น ๆ ตามต้องการ

                ip_of_attack = ipa_temp[0]
                type_of_attack = "Someone try to connect server and get some data"
                return f"Dionaea, {alert}, {date}, {time_str}, {ip_of_attack}, {protocol}, {type_of_attack}\n"
    return None

try:
    with open('/opt/dionaea/var/log/dionaea/dionaea.log') as file1, \
         open('DBcowrie.txt', 'a') as file2, \
         open('DBcowrie_backup.txt', 'a') as file3:
        
        count = 0
        while True:
            try:
                for line in file1:
                    data_log = process_line(line)
                    if data_log:
                        file2.write(data_log)
                        file3.write(data_log)
                        logging.info(data_log.strip())
                time.sleep(20)
            except Exception as e:
                logging.error(f"An error occurred during processing: {str(e)}")
            
            print("loop", count)
            count += 1
except Exception as e:
    logging.error(f"An error occurred: {str(e)}")

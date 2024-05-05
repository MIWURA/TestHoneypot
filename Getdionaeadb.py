import time

file1 = open('/opt/dionaea/var/log/dionaea/dionaea.log')
count = 0
while True:
    file2 = open('DBcowrie.txt','a')
    file3 = open('DBcowrie_backup.txt', 'a')
    for i in file1:
        alert = ""
        if i[0] == "[":
            temp = i.split(' ')
            #temp_colon = temp[1].split(',')
            date = temp[0][1:]
            date = date[4:]+"-"+date[2:][:-4]+"-"+date[:-6]
            time_str = temp[1][:-1]
            if temp[2] == "log_sqlite" :
                if temp[4]=="accepted" and temp[5]=="connection":
    
                    ips_temp = temp[9].split(':')
                    ipa_temp = temp[7].split(':')
                    #protocol = ips_temp[1]
                    if ips_temp[1] == "21":
                        alert = "YELLOW!"
                        protocol = "ftp"
                    elif ips_temp[1] == "42":
                        alert = "YELLOW!"
                        protocol = "nameserver"
                    elif ips_temp[1] == "443":
                        alert = "YELLOW!"
                        protocol = "https"
                    elif ips_temp[1] == "80":
                        alert = "YELLOW!"
                        protocol = "http"
                    elif ips_temp[1] == "5060":
                        alert = "YELLOW!"
                        protocol = "sip"
                    elif ips_temp[1] == "1433":
                        alert = "YELLOW!"
                        protocol = "ms-sql-s"
                    elif ips_temp[1] == "1723":
                        alert = "YELLOW!"
                        protocol = "pptp"
                    elif ips_temp[1] == "9100":
                        alert = "YELLOW!"
                        protocol = "jetdirect"
                    ip_of_attack = ipa_temp[0]
                    type_of_attack  = "Someone try to connect server and get some data"

        if alert != "":
            data_log =  "Dionaea, "+alert+", "+date+", "+time_str+", "+ip_of_attack+", "+protocol+", "+type_of_attack+"\n"
            file2.write(data_log)
            file3.write(data_log)
            print(data_log)
    time.sleep(20)
    
    print("loop",count)
    count += 1
    file2.close
    file3.close
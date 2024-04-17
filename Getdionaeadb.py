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
                    alert = "YELLOW!"
                    ips_temp = temp[9].split(':')
                    ipa_temp = temp[7].split(':')
                    #protocol = ips_temp[1]
                    if ips_temp[1] == "21":
                        protocol = "ftp"
                    elif ips_temp[1] == "42":
                        protocol = "nameserver"
                    elif ips_temp[1] == "443":
                        protocol = "https"
                    elif ips_temp[1] == "80":
                        protocol = "http"
                    elif ips_temp[1] == "5060":
                        protocol = "sip"
                    elif ips_temp[1] == "1433":
                        protocol = "ms-sql-s"
                    elif ips_temp[1] == "1723":
                        protocol = "pptp"
                    elif ips_temp[1] == "9100":
                        protocol = "jetdirect"
                    ip_of_attack = ipa_temp[0]
                    type_of_attack  = "Someone try to connect server and get some data"
            elif temp[2] == "ftp" :
                if temp[4]=="cmd" and temp[5]=="'b'USER''":
                    alert = "RED!"
                    protocol = "ftp"
                    ip_of_attack = "192.168.1.106"
                    type_of_attack  = "Someone try to login server"

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
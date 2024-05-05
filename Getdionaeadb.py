import time

count = 0
while True:
    try:
        with open('/opt/dionaea/var/log/dionaea/dionaea.log') as file1:
            with open('DBcowrie.txt','a') as file2, open('DBcowrie_backup.txt', 'a') as file3:
                for i in file1:
                    alert = ""
                    if i[0] == "[":
                        temp = i.split(' ')
                        if temp[2] == "log_sqlite" :
                            if temp[4]=="accepted" and temp[5]=="connection":
                                date = temp[0][1:]
                                date = date[4:]+"-"+date[2:][:-4]+"-"+date[:-6]
                                time_str = temp[1][:-1]
                                ips_temp = temp[9].split(':')
                                ipa_temp = temp[7].split(':')
                                if ips_temp[1] == "21":
                                    alert = "YELLOW!"
                                    protocol = "ftp"
                                elif ips_temp[1] == "42":
                                    alert = "YELLOW!"
                                    protocol = "nameserver"
                                # Add more conditions for other ports...
                                
                                ip_of_attack = ipa_temp[0]
                                type_of_attack  = "Someone try to connect server and get some data"

                    if alert != "":
                        data_log =  "Dionaea, "+alert+", "+date+", "+time_str+", "+ip_of_attack+", "+protocol+", "+type_of_attack+"\n"
                        file2.write(data_log)
                        file3.write(data_log)
                        print(data_log)
        time.sleep(20)
    except Exception as e:
        print("An error occurred:", str(e))
    
    print("loop",count)
    count += 1

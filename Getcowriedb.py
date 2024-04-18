import time

file1 = open('/home/cowrie/cowrie/var/log/cowrie/cowrie.log')
count = 0
while True:
	file2 = open('DBcowrie.txt','a')
	file3 = open('DBcowrie_backup.txt', 'a')
	for i in file1:
		alert = ""
		temp = i.split(' ')
		#temp_colon = temp[1].split(',')
		date = temp[0][:-17]
		time_str = temp[0][11:][:-8]

		if i[0] == "2":
			temp_colon = temp[1].split(',')
			if temp_colon[0][1:] == "HoneyPotSSHTransport" :
				protocal = "SSH"
				ip_of_attack = temp_colon[2][:-1]
				if temp[2]=="login" and temp[3]=="attempt":
					alert = "RED!"
					temp2 = temp[4].split("'")
					user = temp2[1]
					status = temp[5]
					password = temp2[3]
					type_of_attack  = "Someone try to login server By User: "+user+" Password: "+password+" status: "+status
				elif temp[2]== "Connection" and  temp[3]== "lost" and temp[5]== "0":
					alert = "YELLOW!"
					type_of_attack  = "Someone try to connect server and get some data"
				elif temp[2][:-1]== "CMD" :
					alert = "ORANGE!"
					cmd=temp[3]
					type_of_attack  = "CMD: "+cmd
			elif  temp[1][1:][:-18] == "CowrieTelnetTransport" :
				protocal = "Telnet"
				ip_of_attack = temp[1][26:][:-1]
				if temp[2]== "Connection" and  temp[3]== "lost" :
					alert = "YELLOW!"
					type_of_attack  = "Someone try to connect server and get some data"
				elif temp[2][:-1]== "CMD" :
					alert = "ORANGE!"
					cmd=temp[3]
					type_of_attack  = "CMD: "+cmd
				elif temp[2]=="login" and temp[3]=="attempt":
					alert = "RED!"
					temp2 = temp[4].split("'")
					user = temp2[1]
					status = temp[5]
					password = temp2[3]
					type_of_attack  = "Someone try to login server By User: "+user+" Password: "+password+" status: "+status

		if alert != "":
			data_log =  "Cowrie, "+alert+", "+date+", "+time_str+", "+ip_of_attack+", "+protocal+", "+type_of_attack+"\n"
			file2.write(data_log)
			file3.write(data_log)
			print(data_log)
	time.sleep(1)
	print("loop",count)
	count += 1
	file2.close
	file3.close

file1.close
print("close")
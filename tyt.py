import mysql.connector
import json

counter = 0
db_config = {
        'host' : 'localhost',
        'user' : 'mypot',
        'password' : 'Mypot@123',
        'database' : 'mypot'
    }


def getDB(data):
    data_list = data.split(", ")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sqlqurey = 'INSERT INTO honeypot(type, alert, date, time, ip_attacker, ip_server, protocol, comment) VALUES ("' + data_list[0] + '","' + data_list[1] + '","' + data_list[2] + '","' + data_list[3] + '","' + data_list[4] + '","192.168.1.111","' + data_list[5] + '","' + data_list[6] + '")'
    cursor.execute(sqlqurey)
    print('commit')
    conn.commit()

def submit():
    global counter
    with open("DBcowrie.txt","r+") as f:
        for line in f.readlines():
            getDB(line)
            print(line)
            print(counter)
            counter+=1
    

if __name__ == '__main__':
    submit()
    

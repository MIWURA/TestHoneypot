#!/bin/bash

nohup /usr/bin/python /home/os/TestHoneypot/log/reset.py &
nohup /usr/bin/python /home/os/TestHoneypot/log/Getcowriedb.py &
nohup /usr/bin/python /home/os/TestHoneypot/log/Getdionaeadb.py &
nohup /usr/bin/python /home/os/TestHoneypot/log/insertDB.py &
nohup /usr/bin/python /home/os/TestHoneypot/app.py &

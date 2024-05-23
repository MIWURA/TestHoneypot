#!/bin/bash

/usr/bin/python /home/os/TestHoneypot/log/reset.py &
/usr/bin/python /home/os/TestHoneypot/log/Getcowriedb.py &
/usr/bin/python /home/os/TestHoneypot/log/Getdionaeadb.py &
/usr/bin/python /home/os/TestHoneypot/log/insertDB.py &
/usr/bin/python /home/os/TestHoneypot/app.py &

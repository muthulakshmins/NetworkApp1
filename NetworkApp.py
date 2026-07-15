#Importing the necessary modules

import sys
import time
from ip_file_valid import ip_file_valid
from ip_addr_valid import ip_addr_valid
from ip_reach import ip_reach
from ssh_connection import ssh_connection
from create_threads import create_threads

#step1: Saving the list of ip address in ip_file.txt to a variable ip_list
ip_list  = ip_file_valid()

#step2: Verify the validity of each IP address in the list ip_list
try:
    ip_addr_valid(ip_list)
except KeyboardInterrupt:
    print("\n\n Program aborted by user.. Exiting ....")

#step3: Verifying the reachablity of each IP address in the list
try:
    ip_reach(ip_list)
except KeyboardInterrupt:
    print("\n\n Program aborted by user.. Exiting ....")

#step4: Creating the threads for one or multiple SSH connections

#Using while True infinite loop to keep the program alive and running until the user stops by pressing cntrl+c
while True:              
    create_threads(ip_list,ssh_connection)
    time.sleep(3)

#End of program
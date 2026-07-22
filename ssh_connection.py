#This script has 3 sections
#Section1: Check username and password file exits and valid in the local file system
#Section2: Check commands file exist in the local file system
#Section3: SSH connection function that performs connecting to device, sending the commands and storing output

import paramiko
import os
import time
import sys
import re
from datetime import datetime

#Section1:
#step1: Prompt user for input - USERNAME and PASSWORD file
#user_file = input("\n Enter the user file path (e.g. D:\MyApp\Myfile.txt) ") 
user_file = "D:\\NetworkApp_1\\user.txt"
print("User file path : D:\\NetworkApp_1\\user.txt" )

#step2: Verify if the file exists or not 
if os.path.isfile(user_file) == True:
    print("User login file {} exist".format(user_file))
else:
    print("User login file {} does not exists !!. Please check and try again !!".format(user_file))
    sys.exit()
##############################################################
    
#Section2:
#step1: Prompt user for input - COMMANDS file
#cmd_file = input("\n #Enter the command file path (e.g. D:\MyApp\Myfile.txt) ") 
cmd_file = "D:\\NetworkApp_1\\cmd.txt"
print("Commands file path : D:\\NetworkApp_1\\cmd.txt" )

#step2: Verify if the file exists or not 
if os.path.isfile(cmd_file) == True:
    print("Commands file {} exist".format(cmd_file))
else:
    print("Commands file {} does not exists !!. Please check and try again !!".format(cmd_file))
    sys.exit()

###############################################################

#Section3

def ssh_connection(ip):
    
    global user_file
    global cmd_file
    
    #step1: creating the ssh connection
    try:
        #Define ssh parameters
        selected_user_file = open(user_file,'r')
        
        #Starting from beginning of the file
        selected_user_file.seek(0)
        
        #Reading the username from the file
        username = selected_user_file.readlines()[0].split(',')[0].rstrip('\n')
        
        #Starting from beginning of the file
        selected_user_file.seek(0)
        
        #Reading the password from the file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip('\n')
        
        #Logging into the device
        session = paramiko.SSHClient()
        
        #This is used to auto-accept the unknown host keys from servers so that the program can run without any interupption
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        #Connect to the device
        session.connect(ip.rstrip('\n'), username = username, password = password)
        
        #Start the interactive shell session on the router to reach the CLI
        connection = session.invoke_shell()      # creating object of the invoke_shell method of SSHClient class
        
        #Setting terminal length for the entire output - disable pagination
        connection.send("enable\n")
        connection.send("terminal length 0\n")
        time.sleep(1)
        
        #Entering the global config mode
        connection.send('\n')
        connection.send('config terminal\n')
        connection.send('exit\n')
        time.sleep(1)
            
        #Open the cmd file for reading the commands
        selected_cmd_file = open(cmd_file,'r')
        
        #Start from beginning of file
        selected_cmd_file.seek(0)

        #Write each line from cmd file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(5)
        
        #Close the user file
        selected_user_file.close()

        #Close the command file
        selected_cmd_file.close()
        
        #Checking for command output for IOS syntax errors using regular expression
        router_output = connection.recv(65535).decode('utf-8')
        
        if re.search('Invalid input',router_output):
            print("There is atleast one IOS syntax error on device {}".format(ip))
        
        else:
            print("\n Done !! Commands successfully sent to the device {}".format(ip))

        #Print the clean command output
        start = str(router_output).find('Cisco-R')    # To print output from hostname Cisco-R
        #output = router_output.replace("\r\n", "\n")
        output = router_output[start:]
           
        os.makedirs("logs",exist_ok = True)
        filename = f"logs\\{ip}.log"
        filename = f"logs\\{ip.strip()}.log"
        
        with open(filename, 'w') as logfile:    #Overwrite the log file everytime we run the code
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logfile.write("=" * 60 + "\n")
            logfile.write(f"Time    : {timestamp}\n")
            logfile.write(f"Device  : {ip.strip()}\n")
            logfile.write("=" * 60 + "\n")
            logfile.write(output)
            logfile.write("\n\n")
        
        print(f'Output saved to file {filename}')
        
        ip = re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", str(output))  # we need to convert this output list into str to pass as arg in findall() function
        #print(f"The list of interface IP address :{ip}")
        loopback_ips = re.findall(r"(Loopback\d+)\s+(\d{1,3}(?:\.\d{1,3}){3})",output)
        #print(loopback_ips)
        for interface, ip in loopback_ips:
            print(f"{interface} : {ip}")

        print("End of program :)")
        
        #Closing the connection
        session.close()
        

    except paramiko.AuthenticationException:
        print(" Invalid username and password.. Please check username/password and device configuratio")
        print("Closing the program ...BYE....")
        

#NetworkApp_1: 
#script_1: ip_file_valid checking

#step1: Import modules os and sys
import os.path
import sys

def ip_file_valid():
#step2: Input the file path  of the file that has list of ip addresses 
    #ip_file = input("Enter the file path: ")
    ip_file = r"D:\\NetworkApp_1\\ip_file.txt"                  

#step3: Check if the file exists or not using isfile method frpm os.path module
    if os.path.isfile(ip_file) == True:
        print("IP File is valid!! \n")
    else:
        print("IP File does not exist. Please check and try again !!",format(ip_file))
        sys.exit()
        
#step4: Open the file in read mode and read lines
    with open(ip_file,"r") as selected_ip_file:   #with keyword is used to close file automatically
        selected_ip_file.seek(0)                  #to bring the cursor to start of the file
        ip_list = selected_ip_file.readlines()    #add the read lines to a list (ip_list)

    return ip_list

    

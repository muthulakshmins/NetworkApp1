import sys
import subprocess

def ip_reach(list):
    
    for ip in list:
        ip = ip.rstrip('\n')
        
        ping_reply = subprocess.call(f'ping {ip} -n 2', stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
        
        if ping_reply == 0:
            print(f"\n* {ip} is reachable :)".format(ip))
            continue
        else:
            print(f"\n* {ip} is not reachable !!!!! :( Check the connection and try again ... ".format(ip))
            sys.exit()
          
            
        
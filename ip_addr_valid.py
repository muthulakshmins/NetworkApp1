import sys

#Checking the octets
def ip_addr_valid(ip_list):
        
    for ip in ip_list:
        ip = ip.rstrip("\n")    #Remove new line    
        octet_list = ip.split('.')
        
        #check there are four octets first
        if (len(octet_list) != 4):
            print(f"Invalid IP Address : {ip}")
            sys.exit()
        
        try:
            first  = int(octet_list[0])
            second = int(octet_list[1])
            third  = int(octet_list[2])
            fourth = int(octet_list[3])
        
        except ValueError:
            print(f"Invalid IP Address : {ip}. IP not having intergers !!")
        
        if (1 <= first <= 223) and (first != 127) and (first != 169 or second != 254) and (0 <= second <= 255) and (0 <= third <= 255) and (0 <= fourth <= 255):
            continue
        
        else:
            print(f"Invalid IP address: {ip}")
            sys.exit()
            

''' 
the reserved ip address are 
Loopback:   127.0.0.0  - 127.255.255.255
Multicast:  224.0.0.0 - 239.255.255.255
Broadcast:  255.255.255.255
Link local: 169.254.0.0 - 169.254.255.255
Future use: 240.0.0.0 - 255.255.255.254

Valid IP address example:
192.168.1.1
169.1.1.1 is allowed

Octet validation:
1) len(octet_list) == 4    #Length of the Ip address should be four
Valid: 192.168.1.1
Invalid: 192.168.1

2) 1 <= first <= 223   #First Octet check
Allows:
1
2
10
100
223
Rejects:
0
224
240
255
Why?
224-239 → Multicast
240-255 → Reserved
0.x.x.x → Reserved


3) first != 127    #Rejects Loopback
Rejects:
127.0.0.1
127.1.1.1

4) (first != 169 or second != 254)
Reject link local address
169.254.x.x  ..They are Automatic Private IP addressing
169.254.1.1, 169.254.200.10

But 169.1.1.1 is allowed

5) 0 <= second <= 255  #Remaining octets
Each must be between 0 and 255


''' 

import socket,subprocess,sys
from datetime import datetime
"""
This is Sequntial Port Scanner
"""

#Clear the screen
subprocess.call('clear',shell=True)

remoteServerIP=0
remoteServer=""

def checkhost(remoteServert):
    try:
        #Asking for input and translate the input to IPV4 adress format
        remoteServer = input("Enter a remote host to scan: ")
        return socket.gethostbyname(remoteServer)
    except socket.gaierror:
        print("\n invalid Address, exapmle: www.example.com")
        return 0
    
while remoteServerIP==0:
    remoteServerIP = checkhost(remoteServer)


print ("-" * 60)
print ("Please wait, scanning remote host "+ remoteServerIP)
print ("-" * 60)

# Check what time the scan started
t1 = datetime.now()

try:
    for port in range(1,1025):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP,port)) #returns error indicator
        if result == 0:
            print ("Port {} is open".format(port))
except KeyboardInterrupt:
    print("\n You pressed Ctrl+C, Exiting Program")
    sys.exit()
except socket.gaierror:
	print("Hostname could not be resolved.")
	sys.exit()
except socket.error:
	print("Could not connect to server")
	sys.exit()

# Printing time information to screen
print ('Scanning Completed in: '+str(datetime.now().microsecond-t1.microsecond)+" ms")        
        


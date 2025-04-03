import threading, socket, sys,subprocess
from queue import Queue
from datetime import datetime
import os
import sys
import subprocess
"""
This is Threaded Port Scanner
"""

#Clear the screen
subprocess.call('clear',shell=True)

# a print_lock is what is used to prevent "double" modification of shared variables.
# similar to volatile varibale in java
print_lock = threading.Lock()

#Varibales
remoteServerIP=0
mode=0
remoteServer=""
queue = Queue() #Queue for holding the range of port to scan 
open_ports = [] #List for holding all the open port

def kill_process_on_port(port: int):
    """
    Kill the process using the specified port on Windows or Linux.
    """
    try:
        if sys.platform.startswith("win"):  # Windows
            result = subprocess.run(
                ["netstat", "-ano"], capture_output=True, text=True, check=True
            )
            for line in result.stdout.splitlines():
                if f":{port} " in line:
                    pid = line.strip().split()[-1]
                    subprocess.run(["taskkill", "/PID", pid, "/F"], check=True)
                    print(f"Killed process {pid} on port {port}")
                    return
        else:  # Linux / Mac
            result = subprocess.run(
                ["lsof", "-i", f":{port}"], capture_output=True, text=True
            )
            for line in result.stdout.splitlines():
                parts = line.split()
                if parts[1].isdigit():
                    pid = parts[1]
                    subprocess.run(["kill", "-9", pid], check=True)
                    print(f"Killed process {pid} on port {port}")
                    return
        print(f"No process found on port {port}")
    except Exception as e:
        print(f"Error: {e}")

def portscan(port,remoteServerIP):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect_ex((remoteServerIP,port))
        return True
    except:
        return False
    
#cheicking the input from user
def checkhost(remoteServert):
    try:
        #Asking for input and translate the input to IPV4 adress format
        remoteServer = input("Enter a remote host to scan: ")
        return socket.gethostbyname(remoteServer)
    except socket.gaierror:
        print("\n invalid Address, exapmle: www.example.com")
        return 0

#define the ports we want to scan, for speeding the process
def get_ports(mode):
    if int(mode) == 1:
        for port in range(1, 1024):
            queue.put(port)
    elif int(mode) == 2:
        for port in range(1, 49152):
            queue.put(port)
    elif int(mode) == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)
    elif int(mode) == 4:
        while True:
            count=0
            ports = input("Enter your ports (seperate by blank):")
            ports = ports.split()
            for i in ports:
                if i.isdigit() and int(i)>0:
                    count+=1
            if count==len(ports):break
            print("Invalid Input Please Enter ports number as postive integer seperated by blank")
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)
          
# This function will be responsible for getting the port numbers from the queue,
# scanning them and printing the results.    
def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port,remoteServerIP):
            print("Port {} is open!".format(port))
            open_ports.append(port)


# This Function accept two Parameters:
#   1)threads - is for the amount of threads we want to start and the 
#   2)mode - scanning mode
def run_scanner(threads, mode):

    get_ports(mode)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("*"*60)
    print("Open ports are:", open_ports)
    print("*"*60)


while remoteServerIP==0:
    remoteServerIP = checkhost(remoteServer)
print ("-" * 60)
print("\n Please Select your scanning mode:")
print("\n   1 - Scan which port is open in the range of 1 - 1024")
print("\n   2 - Scan which port is open in the range of 1 - 49152")
print("\n   3 - Common Port [20, 21, 22, 23, 25, 53, 80, 110, 443]")
print("\n   4 - Manual Port input")
while True:
    mode = input("Your selection:")
    if mode.isdigit() and 1<= int(mode) <=4:
        break
    print ("Invalid Input please choose a number between 1-4")
print("-"*60)
while True:
    threadNum = input("\n Please enter number of threads:")
    if threadNum.isdigit() and int(threadNum) >0:
        break
    print ("Invalid Input please choose a number between above 0")
t1 = datetime.now()
run_scanner(10,mode)
print ('Scanning Completed in: '+str(datetime.now().microsecond-t1.microsecond)+" ms")

import time
import os
import subprocess

import conf
from client import ssl_client


def request():
    print("\nAuthentication and message")
    user = input("Enter user: ")
    password = input("Enter pass: ")
    msg = input("Enter message: ")

    print("\nUser: "+user+" Message: "+ msg)
    print("Sending message...")

    host_ip, server_port = "127.0.0.1", 9999
    ssl_client(host_ip, server_port,user,password,msg).connect()

if __name__ == "__main__":    
    print("Welcome to INSEGUS' configuration environment\n \
            \nWhat would you like to do?")

    print("[1] Turn on the system")
    print("[2] Set audit period")
    print("[3] Server audit")
    print("[4] Exit configuration\n")

    case = int(input("Choose option: "))
        
    while case >4 or case==0:
        case = int(input("You can choose between [1 | 2 | 3], choose option: "))

    if case == 1:
        print("Turning on the system...")
        print("Turning on the server...\n")

        e = subprocess.Popen("server.exe" ,shell=True)
  
        print("\nWaiting for PEM")
        time.sleep(6)

        if e.poll() is None:
            request()
            time.sleep(2)
            t = input("Do you want to send any other message? [Y/N]")
            if t == "Y" or t == "y":
                while True:
                    request()
                    t1  = input("Do you want to send any other message? [Y/N]")
                    if t1 == "N" or t1 == "n" :
                        break
            else:
                print("\nTurning off the system...")
                os.system("taskkill /f /im  server.exe")
                time.sleep(6)
                exit()

        else:
            print("\nFailed introducing PEM")
            time.sleep(6)
            exit()
    
    elif case == 2:
        print("Setting audit period...")
        print("Daily reviews are perfomed")
        hday = input("Set revision time: ")
        os.system(conf.TASKSC+hday)

    elif case == 3:
        print("Performing server audit...")
        print("It may take a few seconds...")
        subprocess.run("reports.exe")
        
    else:
        print("Leaving...")
        time.sleep(1)
        exit(0)

    




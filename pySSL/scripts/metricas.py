import subprocess
import os
import random
import time
from client import ssl_client

user1 = "pabgalace"
user = "pepe"
password = "12345"
msg = "Canales te echamos de menos :("
host_ip, server_port = "127.0.0.1", 9999

tiempo1 = time.time()
x = random.random()
i = 0
while(i<300):

    try:
        ssl_client(host_ip, server_port,user1,password,msg).connect()
    except Exception as e:
        print(e)

    print(i)
    i = i+1

tiempo2 = time.time()

tiempo = tiempo2-tiempo1
print(tiempo)
os.system("taskkill /f /im  server.exe")
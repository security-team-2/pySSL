import subprocess
import os
import random
import time
from client import ssl_client
import matplotlib.pyplot as plt
import numpy as np
user1 = "pabgalace"
user = "pepe"
password = "12345"
msg = "Canales te echamos de menos :("
host_ip, server_port = "127.0.0.1", 9999


def prueba_300():
    res = {}
    tiempo1 = time.time()
    x = random.random()
    i = 0
    j=0
    while(i<300):

        try:
            j+=1
            tiempo_iteracion = time.time()
            ssl_client(host_ip, server_port,user1,password,msg).connect()
            if(i>1) : tiempo_finiter = time.time(); res[i] = tiempo_finiter-tiempo_iteracion
        except Exception as e:
            print(e)

        print(i)
        i = i+1

    tiempo2 = time.time()

    tiempo_total = tiempo2-tiempo1
    print(tiempo_total)
    os.system("taskkill /f /im  server.exe")
    print(res)
    return res
def avg_metric_graph():
    """
    Returns a bar graph showing the access time of 100 regular messages and 100 MitM modified messages alongside their average values
    """
    regular_time_access = prueba_300()


    x = list(regular_time_access.keys())
    y = list(regular_time_access.values())
    co = np.arange(len(x))
    
    #plt.bar(co-0.2,y,width=0.4,color = "lightskyblue",label="regular msgs")
    #plt.bar(co+0.2,y1,width=0.4, color = "lightcoral", label= "MitM msgs")
    #plt.bar(regular_time_access.keys(), regular_time_access.values(),width=0.4, color = "lightcoral", label= "MitM msgs")
    plt.plot(regular_time_access.keys(), regular_time_access.values())
    plt.xlabel("Server messages ")
    plt.ylabel("Response time (seconds)")
    plt.title("Server Performance Test (100 messages)")

    plt.axhline(y=np.nanmean(y), color='black', linestyle='--', linewidth=3, label= "avg regular msg ="+(str(round(np.nanmean(y)*1000))+" miliseconds"))
    plt.legend()
    plt.show()


avg_metric_graph()
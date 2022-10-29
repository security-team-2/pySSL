import os
import time
from client import ssl_client
import matplotlib.pyplot as plt
import numpy as np


user1 = "anarodlop12"
user = "pepe"
password = "betis"
msg = "Canales te echamos de menos :("

host_ip, server_port = "127.0.0.1", 9999

def test_300():
    res = {}
    t1 = time.time()
    i = 0
    j = 0
    while(i<300):
        try:
            j+=1
            iteration_time = time.time()
            ssl_client(host_ip, server_port, user1, password, msg).connect()
            if(i>1): finish_time = time.time(); res[i] = finish_time-iteration_time
        except Exception as e:
            print(e)

        print(i)
        i = i+1

    t2 = time.time()

    total_time = t2-t1
    print(total_time)
    os.system("taskkill /f /im  server.exe")
    print(res)
    return res, total_time

def avg_metric_graph():
    """
    Returns a dotted line graph showing the server response time when sending 300 messages along with average response time
    """
    regular_time_access, total_t = test_300()

    y = list(regular_time_access.values())

    plt.plot(regular_time_access.keys(), regular_time_access.values())

    plt.xlabel("Server messages")
    plt.ylabel("Response time (seconds)")
    plt.title("Server Performance Test "+str(total_t)+" seconds")

    plt.axhline(y=np.nanmean(y), color='black', linestyle='--', linewidth=3, label= "avg response time ="+(str(round(np.nanmean(y)*1000))+" miliseconds"))
    plt.legend()
    plt.show()


avg_metric_graph()
import socket
import ssl
import time

import conf


host_ip, server_port = "127.0.0.1", 9999

class ssl_client():

    def __init__(self, host_ip, server_port, user, password, msg):
        self.host_ip = host_ip                                                                                 
        self.server_port = server_port   
        self.user = user
        self.password = password                                                                              
        self.msg = msg                                                                                  

    def connect(self):
        
        purpose = ssl.Purpose.SERVER_AUTH # Passing this as the purpose sets verify_mode to CERT_REQUIRED 
        context = ssl.create_default_context(purpose, cafile=conf.CLNT_CERT_AT) # Returns a context with default settings and loads specific CA certificates if given or loads default CA certificates
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_ssl = context.wrap_socket(client,server_hostname=host_ip)
        # Let socket wrap correctly

        client_ssl.connect((host_ip,server_port))

        self.data =  "|".join([self.user,self.password,self.msg])
        client_ssl.sendall(self.data.encode())
        self.received = client_ssl.recv(1024).decode("utf-8")
        client_ssl.close()
        print(self.received)
        print(client_ssl.version())

        print ("\nBytes Sent:       {}".format(self.data)+ "\nServer Response: ", self.received)



if __name__ == "__main__":

    user = "pepe"
    password = "12345"
    msg = "Canales te echamos de menos :("

    ssl_client(host_ip, server_port,user,password,msg).connect()
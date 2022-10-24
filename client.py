import socket
import ssl

host_ip, server_port = "127.0.0.1", 9999

class ssl_client():

    def __init__(self, host_ip, server_port, msg):
        self.host_ip = host_ip                                                                                 
        self.server_port = server_port                                                                                 
        self.msg = msg                                                                                  

    def connect(self):
        
        purpose = ssl.Purpose.SERVER_AUTH # Passing this as the purpose sets verify_mode to CERT_REQUIRED 
        context = ssl.create_default_context(purpose, cafile='cert\ca-cert.pem') # Returns a context with default settings and loads specific CA certificates if given or loads default CA certificates
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_ssl = context.wrap_socket(client,server_hostname=host_ip)
        
        client_ssl.connect((host_ip,server_port))

        client_ssl.sendall(self.msg.encode())
        self.received = client_ssl.recv(1024).decode("utf-8")

        print(self.received)
        print(client_ssl.version())

        print ("\nBytes Sent:       {}".format(self.msg)+ "\nBytes Received:   {}".format(self.received.decode()))
        print ("Server Response: ", self.received.decode())

        client_ssl.close()

msg = "Canales te echamos de menos :("
ssl_client(host_ip, server_port, msg)
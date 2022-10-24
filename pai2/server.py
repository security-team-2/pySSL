from copyreg import pickle
import socketserver
import hmac
import hashlib
import time
import secrets
import random
import pickle
import os

import conf
from verifier import Verifier

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    TCP Server class.

    Note:   This class inherits from the class 'socketserver.BaseRequestHandler'.
            The handle method is implemented to exchange data with the client.
    """
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
    
    def handle(self): 
        self.attack_file()
        local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

        self.nonce = secrets.token_urlsafe()
        self.data = self.request.recv(1024).strip().decode()    # Last message received is loaded  
        
        print("\n{} sent:".format(self.client_address[0]))
        self.verif = Verifier(self.data, sv= True)    # Integrity check of the received message
        self.message = local_time +" [SRC_IP: "+self.client_address[0]+"]"+ self.verif.logData + self.data.split("|")[0]
        self.msg= self.verif.msgSv[0]

        if self.verif.msgSv[1] == 0: pass
        elif self.verif.msgSv[1] == 1: self.rep_att +=1
        else: self.mitm_att +=1

        self.server_response()
        self.write_attack()

    def attack_file(self):    # Attack log file
        if os.path.exists(conf.ATTS_FROM_C_TO_S):
            f = open(conf.ATTS_FROM_C_TO_S, "r")
            attack_list = [l.split(":")[1].strip() for l in f]
            self.mitm_att = int(attack_list[0])
            self.rep_att = int(attack_list[1])
            f.close()
        else:
            with open(conf.ATTS_FROM_C_TO_S,"w") as f:
                f.write("mitm_att : 0\nreplay_att : 0")
                f.close()
            self.mitm_att = 0
            self.rep_att = 0

    def write_attack(self):
        attacks =[self.mitm_att, self.rep_att]
        replacement = ""
        f_read = open(conf.ATTS_FROM_C_TO_S, "r")
        i =0
        for line in f_read.readlines():
            s_line = line.split(":")
            replacement += s_line[0]+": "+ str(attacks[i])+"\n"
            i+=1
        f_read.close()
        fout = open(conf.ATTS_FROM_C_TO_S, "w+")
        fout.write(replacement)
        fout.close()

    def server_response(self):
        attack = True
        self.msg2 = self.msg
        if attack == True:
            x = random.random()
            if(x<1/3): 
                self.msg2 = self.msg+" theMANisHERE"
            elif x>= 1/3 and x<2/3: 
                if os.path.exists(conf.NONCE_CLNT):
                    with open(conf.NONCE_CLNT, "rb") as f:
                        self.nonce = pickle.load(f)[-1]
                        f.close()
        
        hash_new =  hmac.new(self.verif.key.encode(),(self.msg+self.nonce).encode(), hashlib.sha256).hexdigest()
        response =  "|".join([self.msg2,self.nonce,hash_new])
        self.request.sendall(response.encode())
        self.log(self.message,True)  
        print("Server Response: ",self.msg2) 

    def log(self,mensaje,display=False):
        """
        Returns by console and writes the log in the log file.
        """
        if display: print(mensaje)        
        with open(conf.LOGS, 'a') as f:
            f.write("\n"+mensaje)
            f.close()

if __name__ == "__main__":

    HOST, PORT = "localhost", 9999
    handler_tcp = Handler_TCPServer  
    tcp_server = socketserver.TCPServer((HOST, PORT), handler_tcp) # TCP server instance, applying the corresponding socket and handler

    try:
        print("Active server (HOST: %s ,PORT: %d)\n" %(HOST, PORT))   # TCP server activation
        tcp_server.serve_forever()                                      # For server abortion press Ctrl-C

    except Exception as e:
        print("Server opening error: ",e)
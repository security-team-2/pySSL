import socket
import ssl
import os
import pickle
import time

import conf

host_ip, server_port = "127.0.0.1", 9999
cipher = 'DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-GCM-SHA256'

class ssl_server():
    def server(self):
        self.attack_file()
        purpose=ssl.Purpose.CLIENT_AUTH # Passing this as the purpose sets verify_mode to CERT_REQUIRED 
        context = ssl.create_default_context(purpose, cafile=conf.SERV_CERT_AT) # Returns a context with default settings and loads specific CA certificates if given or loads default CA certificates

        context.set_ciphers(cipher)
        context.load_cert_chain(conf.SERV_CERT_AT,conf.SERV_PRIV_KEY)
        while True:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host_ip,server_port))

            print(f"server running at '{host_ip}' with '{server_port}'\n ready to accept requests")
            server.listen(3)

            ssl_server= context.wrap_socket(server,server_side=True)
            conn, add = ssl_server.accept()
            print(f"server trying to connec {add}")

            data = conn.recv(1024).strip().decode()
            user, password, msg = data.split("|")

            # Debería existir siempre, dado que los usuarios y pass estarán predefinidos
            if os.path.exists(conf.CREDENTIALS):
                credentials = dict()
                with open(conf.CREDENTIALS,"rb") as f:
                    credentials = pickle.load(f)
                    f.close()

            # Comprobamos que el usuario pertence al servidor
            local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

            if user in credentials.keys():
                if credentials.get(user) == password:
                    conn.send(bytes(f"ACK, welcome to Server ('{host_ip}','{server_port}')...!", "utf-8"))
                    message = local_time +" [SRC_ADDR: "+str(add)+"] [200 ACK] [USER: "+user+"] [PASS: "+password+"] [MSG: "+ msg+"]"
                    self.log(message,True)
                else:
                    conn.send(bytes(f"ERR_PASS ,rejected from Server ('{host_ip}','{server_port}')...!", "utf-8"))
                    message = local_time +" [SRC_ADDR: "+str(add)+"] [401 Unauthorized] [USER: "+user+"] [PASS: "+password+"] [MSG: "+ msg+"]"
                    self.log(message,True)
                    self.pass_err+=1
                    conn.close()
            else:
                conn.send(bytes(f"INVALID_USER, rejected from Server ('{host_ip}','{server_port}')...!", "utf-8"))
                message = local_time +" [SRC_ADDR: "+str(add)+"] [401 Unauthorized] [USER: "+user+"] [PASS: "+password+"] [MSG: "+ msg+"]"
                self.log(message,True)
                self.user_err+=1
                conn.close()
            self.write_attack()
            ssl_server.close()

    def attack_file(self):    # Attack log file
        if os.path.exists(conf.LOG_ERR):
            f = open(conf.LOG_ERR, "r")
            attack_list = [l.split(":")[1].strip() for l in f]
            self.pass_err = int(attack_list[0])
            self.user_err = int(attack_list[1])
            f.close()
        else:
            with open(conf.LOG_ERR,"w") as f:
                f.write("pass_err : 0\nuser_err : 0")
                f.close()
            self.pass_err = 0
            self.user_err = 0

    def write_attack(self):
        attacks =[self.pass_err, self.user_err]
        replacement = ""
        f_read = open(conf.LOG_ERR, "r")
        i =0
        for line in f_read.readlines():
            s_line = line.split(":")
            replacement += s_line[0]+": "+ str(attacks[i])+"\n"
            i+=1
        f_read.close()
        fout = open(conf.LOG_ERR, "w+")
        fout.write(replacement)
        fout.close()

    def log(self,message,display=False):
            """
            Returns by console and writes the log in the log file.
            """
            if display: print(message)        
            with open(conf.LOG, 'a') as f:
                f.write("\n"+message)
                f.close()

     
if __name__ == "__main__":
    ssl_server().server()


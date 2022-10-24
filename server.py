import socket
import ssl

import conf

host_ip, server_port = "127.0.0.1", 9999
cipher = 'DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-GCM-SHA256'

def ssl_server():

    purpose=ssl.Purpose.CLIENT_AUTH # Passing this as the purpose sets verify_mode to CERT_REQUIRED 
    context = ssl.create_default_context(purpose, cafile=conf.SERV_CERT_AT) # Returns a context with default settings and loads specific CA certificates if given or loads default CA certificates

    context.set_ciphers(cipher)
    context.load_cert_chain(conf.SERV_CERT_AT,conf.SERV_PRIV_KEY)
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host_ip,server_port))

        print(f"server running at '{host_ip}' with '{server_port}'\n ready to acept requests")
        server.listen(3)

        ssl_server= context.wrap_socket(server,server_side=True)
        conn, add = ssl_server.accept()
        print(f"server connected to {add}")
        conn.send(bytes(f"welcome to Server ('{host_ip}','{server_port}')...!", "utf-8"))
     
if __name__ == "__main__":
    ssl_server()


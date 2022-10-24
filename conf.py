import os


PATH = os.path.abspath(".")
# Certificados 

# Certificado autoridad servidor
SERV_CERT_AT = os.path.join(PATH,"cert","server-cert.pem")

# Certificado autoridad cliente
CLNT_CERT_AT = os.path.join(PATH,"cert", "ca-cert.pem")

# Clave privada servidor
SERV_PRIV_KEY = os.path.join(PATH,"cert","server-key.pem")

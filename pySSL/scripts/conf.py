import os


PATH = os.path.abspath(".")

SERV_CERT_AT = os.path.join(PATH,"cert","server-cert.pem") # Server authority certificate
CLNT_CERT_AT = os.path.join(PATH,"cert", "ca-cert.pem") # Client authority certificate
SERV_PRIV_KEY = os.path.join(PATH,"cert","server-key.pem") # Server's private key

CREDENTIALS = os.path.join(PATH,"credentials","credentials.pickle") # User and password credentials

PDFS_FOLDER = os.path.join(PATH,"reports")
GRAPHS_FOLDER = os.path.join(PATH,"reports","graphs")

LOG = os.path.join(PATH, "logs", "log.txt")
LOG_ERR = os.path.join(PATH,"logs","err_log.txt")

TASKSC = "SCHTASKS /CREATE /SC DAILY /TN PYSSL\revisionTask /TR " +os.path.join(PATH,"reports.exe")+" /ST "
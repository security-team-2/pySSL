# pySSL

SERVER
 -  Private key
 -  Certificado --> server-cert.pem
 -  Public key --> (en server-cert.pem)
 -  Domains where certificate is valid --> server-ext.cnf 
 -  Server Req --> servidor solicita a la autoridad el certificado

CLIENTE

AUTORIDAD
 - CERTIFICADO AUTORIDAD --> ca-cert.pem
 - PRIVATE KEY -> ca-ker.pem
 - UNICIDAD DE CADA CERTIFICADO (.srl) -> ID DE CADA CERTIFICADO QUE EXPIDE LA AUTOR -> 
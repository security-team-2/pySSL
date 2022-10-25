rm *.pem # removes all pem files before begining

# 1. Generate CA's private key and self-signed certificate (CA Certifier Authority, x509 implies we are self-signing it rather than asking for one)
#    openssl req -x509 -newkey rsa:4096 -days 365 -keyout ca-key.pem -out ca-cert.pem
#    -> key encription: input 1235 for quick tests or -nodes for disabling encription
#    key is encripted, cert is encoded (base64) as it contains public key , identity info and signature and should be visible to eevryone
#    openssl x509 -in ca-cert.pem -noout -text --> this will display all info in the certificate

openssl req -x509 -newkey rsa:4096 -days 365 -keyout ca-key.pem -out ca-cert.pem -subj "/C=ES/ST=Andalusia/L=Dos.Hermanas/O=Chemers/OU=Renfe/CN=Betis/emailAddress=rubenjj99@gmail.com"

echo "CA's self-signed certificate"
openssl x509 -in ca-cert.pem -noout -text

# 2. Generate web server's private key and certificate signing request (CSR)
#    we should change all of the subject info to that of the webserver
#    this key is also encrypted (-nodes to disable it)

openssl req -newkey rsa:4096 -keyout server-key.pem -out server-req.pem -subj "/C=ES/ST=Andalusia/L=Seville/O=security.team.2/OU=security/CN=team.2/emailAddress=rubenjj99@gmail.com"


# 3. Use CA's private key to sign web server's CSR and get back the signed certificate

openssl x509 -req -in server-req.pem -days 365 -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -extfile server-ext.txt

echo "Server's signed certificate"
openssl x509 -in server-cert.pem -noout -text

openssl verify -CAfile ca-cert.pem server-cert.pem  #verifies if certificate is valid
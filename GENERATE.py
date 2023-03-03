import OpenSSL.crypto as crypto
import datetime
import os

# Generate a new private key
pkey = crypto.PKey()
pkey.generate_key(crypto.TYPE_RSA, 2048)

# Generate a new CSR with a subject alternative name for "google.com" and "127.0.0.1"
req = crypto.X509Req()
req.get_subject().CN = "test.com"
san = "DNS:test.com, IP:10.10.10.10"
ext = crypto.X509Extension(b"subjectAltName", False, san.encode())
req.add_extensions([ext])
req.set_pubkey(pkey)
req.sign(pkey, "sha256")

# Generate a new self-signed SSL certificate that includes the "google.com" CN and SAN
cert = crypto.X509()
cert.set_version(2)
cert.set_serial_number(1)
cert.get_subject().CN = "test.com"
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365*24*60*60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(pkey)
cert.add_extensions([ext])
cert.sign(pkey, "sha256")

if(not os.path.exists('certs')):
    os.mkdir('certs')

# Write the certificate and key to disk
with open("certs/server.crt", "wb") as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
with open("certs/server.key", "wb") as f:
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))

# Generate a DER-encoded version of the certificate and key files
cert_der = crypto.dump_certificate(crypto.FILETYPE_ASN1, cert)
with open("certs/server.der", "wb") as f:
    f.write(cert_der)

key_der = crypto.dump_privatekey(crypto.FILETYPE_ASN1, pkey)
with open("certs/key.der", "wb") as f:
    f.write(key_der)

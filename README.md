mongo-ssl
==
Configure a MongoDB server and a PyMongo client
for SSL/TLS using a self-signed certificate.

Creating keys, certificates and a certificate authority
--
Good overview [here](http://dst.lbl.gov/~boverhof/openssl_certs.html).
The following steps pre-suppose that you have `openssl`.
In the following example, I have set the expiration to 10
years by using `-days 3650`. For a shorter expiration, choose
a lower value for the `-days` option.

### Generate a certificate authority

    $ cd ssl
    $ openssl req -out ca.pem -new -x509 -days 3650

Then follow the prompts to enter your information.
This generates the files `ca.pem` and `privkey.pem`.
`ca.pem` is that certificate authority with which new
keys will be generated, and `privkey.pem` is the private key
you use in generating new public and private keys.

If you get the error message `unable to write 'random state'`, change
permissions as suggested [here](http://stackoverflow.com/questions/94445/using-openssl-what-does-unable-to-write-random-state-mean).

### Generate key pair for the mongo server

    $ openssl genrsa -out server.key 2048
    $ openssl req -key server.key -new -out server.req

You will again be prompted to enter your information. The files
`server.key` and `server.req`, together with your certificate
authority and a file `file.srl`, which can be any 2-digit number,
are now used to generate the `server.pem` file, which the server
will use for authentication:

    $ openssl x509 -req -in server.req -CA ca.pem -CAkey privkey.pem -CAserial file.srl -out server.pem -days 3650

You will be prompted to enter the password you used when creating the certificate authority.

### Generate key pair for the client

    $ openssl genrsa -out client.key 2048
    $ openssl req -key client.key -new -out client.req
    $ openssl x509 -req -in client.req -CA ca.pem -CAkey privkey.pem -CAserial file.srl -out client.pem -days 3650

MongoDB configuration
--
1. Make sure mongo is stopped.

PyMongo
--
Example in `./src/connect.py`.

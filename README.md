**Client - Server** authentication demo in python 2.7

#### Main aim of this project was to show how to authenticate user without transferring:
* plain text password
* hashed password
* other value which does not change in subsequent authentication processes

**Solution**: Generate (on server) random nonce value every time user wants to log in. Send nonce to client.
 Client calculates hash(plain_text_password + nonce) and sends it to server. Hash value changes every time and server 
 is able to authenticate user.
 
<pre>
  ______________________                                      ________________________
 |                      |              username              |                        | 
 |                      |----------------------------------->|                        | 
 |                      |         user_salt, nonce           |                        | 
 |                      |<-----------------------------------|                        | 
 |       Client         | hash(nonce + hash(password + salt) |         Server         |
 |                      |----------------------------------->|                        | 
 |                      |        OK | Access Denied          |                        | 
 |                      |<-----------------------------------|                        | 
 |______________________|                                    |________________________|
 
</pre>

Sample User in `sqlite` Database:

    login: admin
    password: Administrator100
    
Run Server

    python run_server.py
Run Client

    python run_client.py

Connection between client and server secured with SSL from OpenSSL library.

##### Server provide:
* login
* register
* for logged users:
    * fake access
    * delete_account
    * change_password

##### Register function:
* client sends username
* server check if username is free and response
* client sends to server password as a text twice
* server checks if passwords match
* server checks if password has enough strength
* server generates salt value
* server hashes (password + salt)
* server save hashed_value and salt in database

##### Login function:
* client sends username
* server respond with client_salt and generated nonce value
* client hashes (password + salt)
* client hashes (nonce + hash(password + salt))
* client sends hashed_value
* server hashes (nonce + hash_from_database)
* if hashes match server grants access





#run server with secure connection
import socket
from OpenSSL import SSL

import src.database as database
import config
from src.server import ClientHandler

context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('keys/key')
context.use_certificate_file('keys/cert')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                   # create a socket object
s = SSL.Connection(context, s)                                          # secure connection

s.bind((config.IP, config.PORT))                                        # bind to the port

s.listen(5)                                                             # wait for client connection.
database.create_table()                                                 # create table if not exist on application start

while True:
    client_socket, address = s.accept()                                 # Establish connection with client
    clientThread = ClientHandler(client_socket)                         # create a thread for each user
    clientThread.start()                                                # run thread

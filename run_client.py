
import socket
import ssl

import config
from src.client import Client

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
s = ssl.wrap_socket(s)                                        # wrap socket to secure connection

s.connect((config.IP, config.PORT))                           # connect to sever

client = Client(s)                                            # create new client object
client.handle_connection()                                    # handle connection with server

__author__ = 'jkordas'

import getpass
import sys

import config
import actions
import passwords


class Client:
    """
    Simple client class to handle connection to server
    """

    def __init__(self, _socket):
        self.socket = _socket
        self.nonce = 0
        self.salt = 0
        self.nonce_send = False

    def send(self, message):
        """
        sends message through socket to server
        """
        try:
            self.socket.send(message)
        except:
            print "Unexpected error:", sys.exc_info()[0]

    def receive(self):
        """
        receives and returns message from server
        """
        input_line = None
        try:
            input_line = self.socket.recv(config.BUFFER_SIZE)
        except:
            print "Unexpected error:", sys.exc_info()[0]

        return input_line

    def take_action(self, action_name):
        """
        decides on base of action_name what action should be taken
        in some actions sends respond to the server
        """
        if action_name == actions.QUIT_ACTION or len(action_name) == 0:
            return
        elif action_name == actions.USERNAME_ACTION:
            input_line = raw_input("Username: ")                    # get username
        elif action_name == actions.PASSWORD_ACTION:
            input_line = getpass.getpass("Password: ")              # get password (with no echo)
            if self.nonce_send:
                hashed_password = passwords.hash_password(input_line, self.salt)[0]      # hash pass
                input_line = passwords.hash_password(hashed_password, self.nonce)[0]     # add nonce and hash again
                self.nonce_send = False
        elif action_name == actions.OLD_PASSWORD_ACTION:
            input_line = getpass.getpass("Old_password: ")          # get password (with no echo)
        elif action_name == actions.NEW_PASSWORD_ACTION:
            input_line = getpass.getpass("New_password: ")          # get password (with no echo)
        elif action_name == actions.TYPE_ACTION:
            input_line = raw_input(">> ")                           # get action type
        elif action_name.find(actions.NONCE_ACTION) != -1:
            action, salt_value, nonce_value = action_name.split(':')
            self.salt = salt_value
            self.nonce = nonce_value
            self.nonce_send = True
            return
        else:                                                       # other communicate from server
            print action_name                                       # show it
            return

        if len(input_line) == 0:
                input_line = "__"
        self.send(input_line)                                       # send answer to server if needed

    def handle_connection(self):
        """
        main function to handle connection with server
        """

        action_name = "_"
        while action_name != actions.QUIT_ACTION and len(action_name) != 0:
            action_name = self.receive()

            actions_array = action_name.splitlines()

            for action in actions_array:
                self.take_action(action)
        print "Connection closed"
        self.socket.close()                                          # Close the socket when done

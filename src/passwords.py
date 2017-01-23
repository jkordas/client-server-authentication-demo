__author__ = 'jkordas'

import uuid                 # to generate salt value
import re                   # to check password with regex
import hashlib              # to hash password


def is_password_valid(password):
    """
    Returns True if password is valid - contains:
     - number
     - lowercase letter
     - uppercase letter
     - length > 7
     otherwise returns False
    """

    if len(password) < 8:
        return False

    #digit check
    pattern = ".*\d.*"
    pattern_compiled = re.compile(pattern)
    result = pattern_compiled.match(password)
    if not bool(result):
        return False

    #lowercase check
    pattern = ".*[a-z].*"
    pattern_compiled = re.compile(pattern)
    result = pattern_compiled.match(password)
    if not bool(result):
        return False

    #uppercase check
    pattern = ".*[A-Z].*"
    pattern_compiled = re.compile(pattern)
    result = pattern_compiled.match(password)
    if not bool(result):
        return False

    #all conditions filled
    return True


def hash_password(password, salt):
    """
    creates sha 256 bit hash
    returns tuple (hash(salt+ password), salt)
    """
    return (hashlib.sha256(salt.encode() + password.encode()).hexdigest(), salt)

def hash_password_generate_salt(password):
    """
    creates sha 256 bit hash
    returns tuple (hash(salt+ password), salt)
    """
    salt = get_salt()                                               # generate a random number
    return (hashlib.sha256(salt.encode() + password.encode()).hexdigest(), salt)

def check_password(hashed_password, salt, user_password):
    """
    check if hash_password equals hash(salt, user_password)
    """
    return hashed_password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

def get_salt():
    """
    generates unique salt value
    """
    return uuid.uuid4().hex
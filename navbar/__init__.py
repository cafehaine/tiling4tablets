__connection = None

def set_connection(conn):
    global __connection
    __connection = conn

def get_connection():
    global __connection
    return __connection

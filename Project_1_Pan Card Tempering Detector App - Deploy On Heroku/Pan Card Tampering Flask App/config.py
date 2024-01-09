import os
from   os import environ

class Config(object):
    
    DEBUG = False       # Debugging mode
    TESTING = False     # Testing mode
    
    #       -------  this part gets the directory where the current file is located.  -------------
    # __file__ :  is a special variable in Python that holds the path to the current file being executed.
    # os.path.dirname() : takes a path and returns the directory containing it.
    # os.path.abspath() : takes a path and converts it to an absolute path, meaning a full path starting from 
    #                     the root directory of the filesystem.
    # os.path.abspath(os.path.dirname(__file__)) : This ensures that the path obtained is absolute, converting 
    #                                              any relative path components to an absolute path. The result 
    #                                              is assigned to the variable basedir.
    basedir    = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = 'sencs01'

    # ----- Database setting --------
    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "test01"

    UPLOADS = "/home/username/app/app/static/uploads"

    SESSION_COOKIE_SECURE = True        # A flag indicating whether the session cookie should only be sent over HTTPS. 
                                        #  This enhances the security of the session.
    DEFAULT_THEME = None


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "test01"

    UPLOADS = "/home/username/app/app/static/uploads"
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    DEBUG = True

    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "test01"

    UPLOADS = "/home/username/app/app/static/uploads"
    SESSION_COOKIE_SECURE = False

 
class DebugConfig(Config):
    DEBUG = False
